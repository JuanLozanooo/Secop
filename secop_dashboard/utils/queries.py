from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sqlalchemy import text

from db import get_engine

TABLE_NAME = "secop"

DISPLAY_COLUMNS = [
    "Entidad",
    "Nit Entidad",
    "Departamento Entidad",
    "Ciudad Entidad",
    "OrdenEntidad",
    "Fecha de Publicacion del Proceso",
    "Precio Base",
    "Modalidad de Contratacion",
    "Duracion",
    "Unidad de Duracion",
    "Proveedores Invitados",
    "Proveedores que Manifestaron Interes",
    "Conteo de Respuestas a Ofertas",
    "Proveedores Unicos con Respuestas",
    "Numero de Lotes",
    "Valor Total Adjudicacion",
    "Codigo Principal de Categoria",
    "Tipo de Contrato",
    "Subtipo de Contrato",
    "Estado Resumen",
    "Estado del Procedimiento",
    "Adjudicado",
]

FILTER_COLUMNS = {
    "Departamento Entidad": "departamento",
    "Ciudad Entidad": "ciudad",
    "Modalidad de Contratacion": "modalidad",
    "Tipo de Contrato": "tipo_contrato",
    "Estado Resumen": "estado_resumen",
    "Adjudicado": "adjudicado",
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
            COUNT(DISTINCT {_quoted("Entidad")}) AS unique_entities,
            COUNT(DISTINCT {_quoted("Departamento Entidad")}) AS unique_departments,
            COUNT(DISTINCT {_quoted("Ciudad Entidad")}) AS unique_cities,
            COUNT(DISTINCT {_quoted("Modalidad de Contratacion")}) AS unique_modalities,
            COUNT(DISTINCT {_quoted("Tipo de Contrato")}) AS unique_contract_types,
            COALESCE(SUM(({numeric_expr("Valor Total Adjudicacion")})::numeric), 0) AS total_awarded_value,
            COALESCE(AVG(({numeric_expr("Valor Total Adjudicacion")})::numeric), 0) AS avg_awarded_value,
            COALESCE(AVG(({numeric_expr("Precio Base")})::numeric), 0) AS avg_base_price,
            COALESCE(AVG(({numeric_expr("Proveedores Invitados")})::numeric), 0) AS avg_invited,
            COALESCE(AVG(({numeric_expr("Proveedores Unicos con Respuestas")})::numeric), 0) AS avg_unique_responses,
            COALESCE(AVG(({numeric_expr("Conteo de Respuestas a Ofertas")})::numeric), 0) AS avg_offers
        FROM {TABLE_NAME}
    """
    df = fetch_dataframe(query)
    return df.iloc[0].to_dict()


def get_top_counts(column: str, limit: int = 10) -> pd.DataFrame:
    query = f"""
        SELECT
            COALESCE(NULLIF(TRIM({_quoted(column)}), ''), 'Sin dato') AS label,
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
            COALESCE(NULLIF(TRIM({_quoted(column)}), ''), 'Sin dato') AS label,
            COALESCE(SUM(({numeric_expr(value_column)})::numeric), 0) AS value
        FROM {TABLE_NAME}
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})


def get_yearly_publications(limit: int = 20) -> pd.DataFrame:
    query = f"""
        SELECT
            CASE
                WHEN TRIM({_quoted("Fecha de Publicacion del Proceso")}) ~ '^[0-9]{{4}}'
                THEN SUBSTRING(TRIM({_quoted("Fecha de Publicacion del Proceso")}) FROM 1 FOR 4)
                ELSE 'Sin dato'
            END AS anio,
            COUNT(*) AS value
        FROM {TABLE_NAME}
        GROUP BY 1
        ORDER BY 1
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})


def get_filter_options(column: str, limit: int = 300) -> List[str]:
    query = f"""
        SELECT DISTINCT COALESCE(NULLIF(TRIM({_quoted(column)}), ''), 'Sin dato') AS value
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
    query = f"""
        SELECT
            {_quoted("Entidad")} AS "Entidad",
            {_quoted("Nit Entidad")} AS "Nit Entidad",
            {_quoted("Departamento Entidad")} AS "Departamento Entidad",
            {_quoted("Ciudad Entidad")} AS "Ciudad Entidad",
            {_quoted("OrdenEntidad")} AS "OrdenEntidad",
            {_quoted("Fecha de Publicacion del Proceso")} AS "Fecha de Publicacion del Proceso",
            {_quoted("Precio Base")} AS "Precio Base",
            {_quoted("Modalidad de Contratacion")} AS "Modalidad de Contratacion",
            {_quoted("Duracion")} AS "Duracion",
            {_quoted("Unidad de Duracion")} AS "Unidad de Duracion",
            {_quoted("Proveedores Invitados")} AS "Proveedores Invitados",
            {_quoted("Proveedores que Manifestaron Interes")} AS "Proveedores que Manifestaron Interes",
            {_quoted("Conteo de Respuestas a Ofertas")} AS "Conteo de Respuestas a Ofertas",
            {_quoted("Proveedores Unicos con Respuestas")} AS "Proveedores Unicos con Respuestas",
            {_quoted("Numero de Lotes")} AS "Numero de Lotes",
            {_quoted("Valor Total Adjudicacion")} AS "Valor Total Adjudicacion",
            {_quoted("Codigo Principal de Categoria")} AS "Codigo Principal de Categoria",
            {_quoted("Tipo de Contrato")} AS "Tipo de Contrato",
            {_quoted("Subtipo de Contrato")} AS "Subtipo de Contrato",
            {_quoted("Estado Resumen")} AS "Estado Resumen",
            {_quoted("Estado del Procedimiento")} AS "Estado del Procedimiento",
            {_quoted("Adjudicado")} AS "Adjudicado"
        FROM {TABLE_NAME}
        {where_sql}
        ORDER BY {_quoted("Fecha de Publicacion del Proceso")} DESC NULLS LAST
        LIMIT :limit OFFSET :offset
    """
    params.update({"limit": page_size, "offset": offset})
    return fetch_dataframe(query, params)


def get_table_sample(limit: int = 15000) -> pd.DataFrame:
    query = f"""
        SELECT
            {_quoted("Precio Base")} AS "Precio Base",
            {_quoted("Duracion")} AS "Duracion",
            {_quoted("Proveedores Invitados")} AS "Proveedores Invitados",
            {_quoted("Proveedores que Manifestaron Interes")} AS "Proveedores que Manifestaron Interes",
            {_quoted("Conteo de Respuestas a Ofertas")} AS "Conteo de Respuestas a Ofertas",
            {_quoted("Proveedores Unicos con Respuestas")} AS "Proveedores Unicos con Respuestas",
            {_quoted("Numero de Lotes")} AS "Numero de Lotes",
            {_quoted("Valor Total Adjudicacion")} AS "Valor Total Adjudicacion",
            {_quoted("Modalidad de Contratacion")} AS "Modalidad de Contratacion",
            {_quoted("Tipo de Contrato")} AS "Tipo de Contrato",
            {_quoted("Departamento Entidad")} AS "Departamento Entidad",
            {_quoted("Ciudad Entidad")} AS "Ciudad Entidad",
            {_quoted("Estado Resumen")} AS "Estado Resumen",
            {_quoted("Adjudicado")} AS "Adjudicado"
        FROM {TABLE_NAME}
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})


def insert_record(record: Dict[str, Any]) -> None:
    engine = get_engine()
    payload = {k: (None if v in ("", "Sin dato") else v) for k, v in record.items()}
    df = pd.DataFrame([payload])
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)


def get_distinct_small(column: str, limit: int = 100) -> List[str]:
    return get_filter_options(column, limit=limit)
