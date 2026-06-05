from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sqlalchemy import text

from db import get_engine

TABLE_NAME = "secop"

DISPLAY_COLUMNS = [
    "id_proceso",
    "entidad",
    "nit_entidad",
    "departamento",
    "ciudad",
    "tipo_entidad",
    "fecha_publicacion",
    "anio",
    "mes",
    "trimestre",
    "modalidad_contratacion",
    "tipo_contrato",
    "subtipo_contrato",
    "categoria_compra",
    "duracion_dias",
    "proveedores_invitados",
    "proveedores_interesados",
    "ofertas_recibidas",
    "proveedores_unicos",
    "precio_base",
    "valor_adjudicacion",
    "ahorro_obtenido",
    "porcentaje_ejecucion",
    "nivel_competencia",
    "estado_proceso",
    "adjudicado",
]

FILTER_COLUMNS = {
    "departamento": "departamento",
    "ciudad": "ciudad",
    "modalidad_contratacion": "modalidad",
    "tipo_contrato": "tipo_contrato",
    "estado_proceso": "estado_proceso",
    "adjudicado": "adjudicado",
}


def _quoted(col: str) -> str:
    return f'"{col}"'


def numeric_expr(col: str) -> str:
    q = _quoted(col)
    return (
        f"NULLIF("
        f"REGEXP_REPLACE("
        f"REPLACE(COALESCE(TRIM({q}::text), ''), ',', ''), "
        f"'[^0-9.-]', '', 'g'"
        f"), ''"
        f")"
    )


def _base_where(filters: Dict[str, Optional[str]]) -> Tuple[str, Dict[str, Any]]:
    clauses = []
    params: Dict[str, Any] = {}
    for col, param_name in FILTER_COLUMNS.items():
        value = filters.get(param_name)
        if value and value != "Todos":
            clauses.append(f"{_quoted(col)} = :{param_name}")
            params[param_name] = value
    where_sql = " WHERE " + " AND ".join(clauses) if clauses else ""
    return where_sql, params


def fetch_scalar(query: str, params: Optional[Dict[str, Any]] = None) -> Any:
    engine = get_engine()
    with engine.connect() as conn:
        return conn.execute(text(query), params or {}).scalar()


def fetch_dataframe(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql_query(text(query), engine, params=params or {})


def get_overview_metrics() -> Dict[str, Any]:
    query = f"""
        SELECT
            COUNT(*) AS total_processes,
            COUNT(DISTINCT {_quoted("entidad")}) AS unique_entities,
            COUNT(DISTINCT {_quoted("departamento")}) AS unique_departments,
            COUNT(DISTINCT {_quoted("ciudad")}) AS unique_cities,
            COUNT(DISTINCT {_quoted("modalidad_contratacion")}) AS unique_modalities,
            COUNT(DISTINCT {_quoted("tipo_contrato")}) AS unique_contract_types,
            COALESCE(SUM(({numeric_expr("valor_adjudicacion")})::numeric), 0) AS total_awarded_value,
            COALESCE(AVG(({numeric_expr("valor_adjudicacion")})::numeric), 0) AS avg_awarded_value,
            COALESCE(AVG(({numeric_expr("precio_base")})::numeric), 0) AS avg_base_price,
            COALESCE(AVG(({numeric_expr("proveedores_invitados")})::numeric), 0) AS avg_invited,
            COALESCE(AVG(({numeric_expr("proveedores_unicos")})::numeric), 0) AS avg_unique_responses,
            COALESCE(AVG(({numeric_expr("ofertas_recibidas")})::numeric), 0) AS avg_offers
        FROM {TABLE_NAME}
    """
    df = fetch_dataframe(query)
    return df.iloc[0].to_dict()


def get_top_counts(column: str, limit: int = 10) -> pd.DataFrame:
    query = f"""
        SELECT
            COALESCE(NULLIF(TRIM({_quoted(column)}::text), ''), 'Sin dato') AS label,
            COUNT(*) AS value
        FROM {TABLE_NAME}
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})


def get_top_values(column: str, value_column: str, limit: int = 10) -> pd.DataFrame:
    query = f"""
        SELECT
            COALESCE(NULLIF(TRIM({_quoted(column)}::text), ''), 'Sin dato') AS label,
            COALESCE(SUM(({numeric_expr(value_column)})::numeric), 0) AS value
        FROM {TABLE_NAME}
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})


def get_yearly_publications(limit: int = 20) -> pd.DataFrame:
    # Ahora usamos la columna nativa "anio" en lugar de parsear la fecha
    query = f"""
        SELECT
            COALESCE(NULLIF(TRIM({_quoted("anio")}::text), ''), 'Sin dato') AS anio,
            COUNT(*) AS value
        FROM {TABLE_NAME}
        GROUP BY 1
        ORDER BY 1
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})


def get_filter_options(column: str, limit: int = 300) -> List[str]:
    query = f"""
        SELECT DISTINCT COALESCE(NULLIF(TRIM({_quoted(column)}::text), ''), 'Sin dato') AS value
        FROM {TABLE_NAME}
        ORDER BY 1
        LIMIT :limit
    """
    df = fetch_dataframe(query, {"limit": limit})
    return df["value"].dropna().astype(str).tolist()


def get_filtered_count(filters: Dict[str, Optional[str]]) -> int:
    where_sql, params = _base_where(filters)
    query = f"SELECT COUNT(*) FROM {TABLE_NAME}{where_sql}"
    return int(fetch_scalar(query, params) or 0)


def get_filtered_page(
        filters: Dict[str, Optional[str]],
        page: int = 1,
        page_size: int = 50,
) -> pd.DataFrame:
    where_sql, params = _base_where(filters)
    offset = max(page - 1, 0) * page_size

    # Genera la lista de columnas seleccionadas basada en DISPLAY_COLUMNS
    cols_sql = ",\n            ".join([f'{_quoted(c)} AS "{c}"' for c in DISPLAY_COLUMNS])

    query = f"""
        SELECT
            {cols_sql}
        FROM {TABLE_NAME}
        {where_sql}
        ORDER BY {_quoted("fecha_publicacion")} DESC NULLS LAST
        LIMIT :limit OFFSET :offset
    """
    params.update({"limit": page_size, "offset": offset})
    return fetch_dataframe(query, params)


def get_table_sample(limit: int = 25000) -> pd.DataFrame:
    # He incluido la lista completa de columnas de tu esquema actual
    query = f"""
        SELECT
            id_proceso,
            entidad,
            nit_entidad,
            departamento,
            ciudad,
            tipo_entidad,
            fecha_publicacion,
            anio,
            mes,
            trimestre,
            modalidad_contratacion,
            tipo_contrato,
            subtipo_contrato,
            categoria_compra,
            duracion_dias,
            proveedores_invitados,
            proveedores_interesados,
            ofertas_recibidas,
            proveedores_unicos,
            precio_base,
            valor_adjudicacion,
            ahorro_obtenido,
            porcentaje_ejecucion,
            nivel_competencia,
            estado_proceso,
            adjudicado
        FROM {TABLE_NAME}
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})

def insert_record(record: Dict[str, Any]) -> None:
    engine = get_engine()

    # 1. Preparar y limpiar los datos (como hicimos antes)
    numeric_fields = [
        "precio_base", "valor_adjudicacion", "ahorro_obtenido",
        "porcentaje_ejecucion", "duracion_dias", "proveedores_invitados",
        "proveedores_interesados", "ofertas_recibidas", "proveedores_unicos"
    ]

    clean_record = {}
    for k, v in record.items():
        if v in ("", "Sin dato", None):
            clean_record[k] = None
        elif k in numeric_fields and isinstance(v, str):
            clean_record[k] = float(v.replace(",", ".")) if v else 0
        else:
            clean_record[k] = v

    # 2. Construir el INSERT manualmente para asegurar que apunta a la tabla correcta
    columns = ", ".join([f'"{k}"' for k in clean_record.keys()])
    placeholders = ", ".join([f":{k}" for k in clean_record.keys()])
    sql = text(f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})")

    # 3. Ejecutar con commit explícito
    with engine.begin() as conn:  # engine.begin() hace commit automáticamente al terminar
        conn.execute(sql, clean_record)

def get_distinct_small(column: str, limit: int = 100) -> List[str]:
    return get_filter_options(column, limit=limit)