import math

import streamlit as st

from utils.queries import FILTER_COLUMNS, get_filter_options, get_filtered_count, get_filtered_page

st.title("Consultar registros")

st.write("Usa los filtros para buscar procesos específicos dentro de la tabla SECOP.")

with st.sidebar:
    st.header("Filtros")
    filters = {}
    for db_col, key in FILTER_COLUMNS.items():
        options = ["Todos"] + get_filter_options(db_col, limit=300)
        filters[key] = st.selectbox(db_col, options, index=0)

page_size = st.selectbox("Filas por página", [25, 50, 100, 250], index=1)
current_page = st.number_input("Página", min_value=1, value=1, step=1)

total_rows = get_filtered_count(filters)
total_pages = max(math.ceil(total_rows / page_size), 1)

st.caption(f"Resultados: {total_rows:,} filas | Páginas: {total_pages:,}")

df = get_filtered_page(filters, page=int(current_page), page_size=page_size)

st.dataframe(df, use_container_width=True, hide_index=True)

csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Descargar CSV de esta página",
    data=csv_bytes,
    file_name="secop_filtrado_pagina.csv",
    mime="text/csv",
)

st.info(
    "Por el tamaño de la base, la descarga directa de toda la tabla completa no es recomendable desde el navegador. "
    "Lo ideal es exportar por filtros o generar el archivo limpio desde el ETL."
)
