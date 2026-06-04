import pandas as pd
import plotly.express as px
import streamlit as st

from utils.queries import get_table_sample

st.title("Análisis Predictivo y Tendencias")

st.write(
    "Este módulo explora las tendencias históricas de la contratación y proyecta comportamientos "
    "basados en promedios móviles, de forma rápida y sin depender de modelos estáticos."
)

if st.button("Cargar y Analizar Tendencias"):
    df = get_table_sample(limit=15000)

    required_cols = ["anio", "mes", "valor_adjudicacion", "precio_base"]
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(f"Faltan las siguientes columnas en la base de datos: {missing}")
        st.stop()

    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce")
    df["valor_adjudicacion"] = pd.to_numeric(df["valor_adjudicacion"], errors="coerce").fillna(0)
    df["precio_base"] = pd.to_numeric(df["precio_base"], errors="coerce").fillna(0)

    df_trend = df[(df["anio"] > 2010) & (df["anio"] <= 2030)].copy()

    if df_trend.empty:
        st.warning("No hay suficientes datos válidos para el análisis de tendencias temporales.")
        st.stop()

    st.subheader("Tendencia de Valor Adjudicado (Promedio Móvil)")

    df_grouped = df_trend.groupby(["anio", "mes"])["valor_adjudicacion"].sum().reset_index()
    df_grouped["periodo"] = df_grouped["anio"].astype(str) + "-" + df_grouped["mes"].astype(str).str.zfill(2)
    df_grouped = df_grouped.sort_values(["anio", "mes"])

    df_grouped["Tendencia (Media Móvil 3M)"] = df_grouped["valor_adjudicacion"].rolling(window=3, min_periods=1).mean()

    fig1 = px.line(
        df_grouped,
        x="periodo",
        y=["valor_adjudicacion", "Tendencia (Media Móvil 3M)"],
        labels={"value": "Valor Adjudicado Total ($)", "periodo": "Periodo (Año-Mes)"},
        title="Evolución Histórica y Tendencia del Valor de Contratos"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    st.subheader("Relación: Precio Base vs. Valor Adjudicado")
    st.write(
        "Análisis de cómo se relacionan los presupuestos iniciales con los valores finalmente adjudicados para evaluar márgenes y eficiencia.")

    df_scatter = df_trend[(df_trend["precio_base"] > 0) & (df_trend["valor_adjudicacion"] > 0)]

    fig2 = px.scatter(
        df_scatter,
        x="precio_base",
        y="valor_adjudicacion",
        opacity=0.5,
        log_x=True,
        log_y=True,
        labels={"precio_base": "Precio Base (Escala Log)", "valor_adjudicacion": "Valor Adjudicado (Escala Log)"},
        title="Correlación de Presupuesto vs Adjudicación"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "💡 **Insights:** El uso de promedios móviles nos permite suavizar picos atípicos en meses de alta contratación y observar la dirección real de la curva a largo plazo.")