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

st.title("📊 Dashboard Estratégico SECOP")
st.markdown("Visión general del estado de la contratación, distribución de recursos y participación de proveedores.")

metrics = get_overview_metrics()

# --- SECCIÓN: KPIs PRINCIPALES ---
st.subheader("💡 Indicadores Clave de Rendimiento (KPIs)")

# Fila 1: Métricas de Volumen y Participación
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Procesos", int_fmt(metrics["total_processes"]))
c2.metric("Entidades Únicas", int_fmt(metrics["unique_entities"]))
c3.metric("Promedio Ofertas Recibidas", f'{float(metrics["avg_offers"] or 0):.1f}')
c4.metric("Promedio Proveedores Invitados", f'{float(metrics["avg_invited"] or 0):.1f}')

# Fila 2: Métricas Financieras (Usando el nuevo formato de millones/billones)
c5, c6, c7 = st.columns(3)
c5.metric("Valor Total Adjudicado", money_fmt(metrics["total_awarded_value"]))
c6.metric("Valor Promedio Adjudicado", money_fmt(metrics["avg_awarded_value"]))
c7.metric("Precio Base Promedio", money_fmt(metrics["avg_base_price"]))

st.divider()

# --- SECCIÓN: ANÁLISIS GEOGRÁFICO Y ENTIDADES ---
st.subheader("📍 Entidades y Geografía")
left, right = st.columns(2)

with left:
    df_dep = get_top_counts("departamento", 10)
    if not df_dep.empty:
        fig = px.bar(
            df_dep, x="value", y="label", orientation="h",
            title="Top 10 Departamentos por Cantidad de Procesos",
            text_auto='.2s' # Muestra el valor abreviado dentro de la barra
        )
        fig.update_layout(yaxis_title="", xaxis_title="Procesos", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

with right:
    # NUEVO GRÁFICO: Entidades que más dinero mueven
    df_val_ent = get_top_values("entidad", "valor_adjudicacion", 10)
    if not df_val_ent.empty:
        fig = px.bar(
            df_val_ent, x="value", y="label", orientation="h",
            title="Top 10 Entidades por Presupuesto Adjudicado",
        )
        fig.update_layout(yaxis_title="", xaxis_title="Valor Adjudicado ($)", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- SECCIÓN: ANÁLISIS CONTRACTUAL ---
st.subheader("📑 Modalidades y Estado Contractual")
left, center, right = st.columns(3)

with left:
    df_mod = get_top_counts("modalidad_contratacion", 10)
    if not df_mod.empty:
        # Cambiado a gráfico de dona (hole=0.4) para ver proporciones
        fig = px.pie(df_mod, names="label", values="value", title="Modalidad de Contratación", hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

with center:
    df_tipo = get_top_counts("tipo_contrato", 10)
    if not df_tipo.empty:
        fig = px.pie(df_tipo, names="label", values="value", title="Tipo de Contrato", hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig, use_container_width=True)

with right:
    # NUEVO GRÁFICO: Qué porcentaje de procesos están publicados vs adjudicados
    df_estado = get_top_counts("estado_proceso", 10)
    if not df_estado.empty:
        fig = px.bar(df_estado, x="label", y="value", title="Estado de los Procesos", color="label")
        fig.update_layout(xaxis_title="", yaxis_title="Cantidad", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- SECCIÓN: CATEGORÍAS Y TEMPORALIDAD ---
st.subheader("📅 Tendencias y Sectores de Compra")
left, right = st.columns(2)

with left:
    df_cat = get_top_counts("categoria_compra", 10)
    if not df_cat.empty:
        fig = px.bar(
            df_cat, x="value", y="label", orientation="h",
            title="Top 10 Categorías de Compra",
            color="value", color_continuous_scale="Blues" # Mapa de calor basado en volumen
        )
        fig.update_layout(yaxis_title="", xaxis_title="Cantidad de Procesos", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

with right:
    df_year = get_yearly_publications(20)
    df_year = df_year[df_year["anio"] != "Sin dato"]
    if not df_year.empty:
        # Cambiado a gráfico de área para darle más peso visual a la tendencia
        fig = px.area(
            df_year, x="anio", y="value", markers=True,
            title="Evolución de Procesos Publicados por Año"
        )
        fig.update_layout(xaxis_title="Año", yaxis_title="Procesos")
        st.plotly_chart(fig, use_container_width=True)