import pandas as pd
import plotly.express as px
import streamlit as st

from utils.formatters import int_fmt, money_fmt
from utils.queries import (
    get_overview_metrics,
    get_top_counts,
    get_top_values,
    get_yearly_publications,
)

st.title("Dashboard SECOP")

metrics = get_overview_metrics()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Procesos", int_fmt(metrics["total_processes"]))
c2.metric("Entidades únicas", int_fmt(metrics["unique_entities"]))
c3.metric("Departamentos", int_fmt(metrics["unique_departments"]))
c4.metric("Ciudades", int_fmt(metrics["unique_cities"]))

c5, c6, c7, c8 = st.columns(4)
c5.metric("Valor total adjudicado", money_fmt(metrics["total_awarded_value"]))
c6.metric("Valor promedio adjudicado", money_fmt(metrics["avg_awarded_value"]))
c7.metric("Precio base promedio", money_fmt(metrics["avg_base_price"]))
c8.metric("Proveedores invitados promedio", f'{float(metrics["avg_invited"] or 0):.2f}')

st.divider()

left, right = st.columns(2)

with left:
    df_dep = get_top_counts("departamento", 10)
    if not df_dep.empty:
        fig = px.bar(df_dep, x="value", y="label", orientation="h", title="Top departamentos por procesos")
        fig.update_layout(yaxis_title="", xaxis_title="Cantidad de procesos")
        st.plotly_chart(fig, use_container_width=True)

with right:
    df_val_dep = get_top_values("departamento", "valor_adjudicacion", 10)
    if not df_val_dep.empty:
        fig = px.bar(df_val_dep, x="value", y="label", orientation="h", title="Top departamentos por valor adjudicado")
        fig.update_layout(yaxis_title="", xaxis_title="Valor adjudicado")
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    df_mod = get_top_counts("modalidad_contratacion", 10)
    if not df_mod.empty:
        fig = px.bar(df_mod, x="label", y="value", title="Modalidad de contratación")
        fig.update_layout(xaxis_title="", yaxis_title="Cantidad")
        st.plotly_chart(fig, use_container_width=True)

with right:
    df_tipo = get_top_counts("tipo_contrato", 10)
    if not df_tipo.empty:
        fig = px.bar(df_tipo, x="label", y="value", title="Tipo de contrato")
        fig.update_layout(xaxis_title="", yaxis_title="Cantidad")
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    df_cat = get_top_counts("categoria_compra", 10)
    if not df_cat.empty:
        fig = px.bar(df_cat, x="value", y="label", orientation="h", title="Top categorías")
        fig.update_layout(yaxis_title="", xaxis_title="Cantidad")
        st.plotly_chart(fig, use_container_width=True)

with right:
    df_year = get_yearly_publications(20)
    df_year = df_year[df_year["anio"] != "Sin dato"]
    if not df_year.empty:
        fig = px.line(df_year, x="anio", y="value", markers=True, title="Procesos por año de publicación")
        fig.update_layout(xaxis_title="Año", yaxis_title="Procesos")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Resumen rápido")

summary = pd.DataFrame(
    {
        "Indicador": [
            "Total procesos",
            "Entidades",
            "Departamentos",
            "Ciudades",
            "Modalidades",
            "Tipos de contrato",
        ],
        "Valor": [
            metrics["total_processes"],
            metrics["unique_entities"],
            metrics["unique_departments"],
            metrics["unique_cities"],
            metrics["unique_modalities"],
            metrics["unique_contract_types"],
        ],
    }
)
st.dataframe(summary, use_container_width=True, hide_index=True)