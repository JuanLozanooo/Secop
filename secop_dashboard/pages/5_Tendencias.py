import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.queries import get_table_sample

st.title("📉 Análisis Predictivo y Tendencias")

st.write(
    "Exploración de la eficiencia contractual y tendencias de mercado. "
    "Analizamos promedios móviles, ahorros obtenidos y el nivel de competencia del sistema."
)

if st.button("Generar Informe de Tendencias"):
    df = get_table_sample(limit=25000)  # Aumentamos muestra para mejor precisión

    # Limpieza de datos
    numeric_cols = ["anio", "mes", "valor_adjudicacion", "precio_base", "ahorro_obtenido", "ofertas_recibidas"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # --- 1. Tendencia de Valor y Eficiencia (Ahorro) ---
    st.subheader("Evolución de Valor y Eficiencia")
    df_grouped = df.groupby(["anio", "mes"])[["valor_adjudicacion", "ahorro_obtenido"]].sum().reset_index()
    df_grouped["periodo"] = df_grouped["anio"].astype(str) + "-" + df_grouped["mes"].astype(str).str.zfill(2)
    df_grouped = df_grouped.sort_values(["anio", "mes"])

    # Cálculo de Media Móvil para Valor
    df_grouped["Tendencia (Media 3M)"] = df_grouped["valor_adjudicacion"].rolling(window=3).mean()

    fig_val = go.Figure()
    fig_val.add_trace(go.Bar(x=df_grouped["periodo"], y=df_grouped["valor_adjudicacion"], name="Valor Adjudicado",
                             marker_color='royalblue'))
    fig_val.add_trace(go.Scatter(x=df_grouped["periodo"], y=df_grouped["Tendencia (Media 3M)"], name="Tendencia (3M)",
                                 line=dict(color='red', width=3)))
    fig_val.update_layout(title="Volumen Mensual de Adjudicación", xaxis_title="Periodo", yaxis_title="$")
    st.plotly_chart(fig_val, use_container_width=True)

    # --- 2. Análisis de Competitividad ---
    st.subheader("Dinámicas de Competencia")
    col1, col2 = st.columns(2)

    with col1:
        df_comp = df.groupby("nivel_competencia")["id_proceso"].count().reset_index()
        fig_comp = px.pie(df_comp, names="nivel_competencia", values="id_proceso",
                          title="Distribución de Niveles de Competencia", hole=0.4)
        st.plotly_chart(fig_comp, use_container_width=True)

    with col2:
        fig_box = px.box(df, x="nivel_competencia", y="ofertas_recibidas", color="nivel_competencia",
                         title="Ofertas Recibidas por Nivel de Competencia")
        st.plotly_chart(fig_box, use_container_width=True)

    # --- 3. Insights Detallados Automáticos ---
    st.divider()
    st.subheader("💡 Insights Estratégicos")

    avg_ahorro = df["ahorro_obtenido"].sum() / df["valor_adjudicacion"].sum() if df[
                                                                                     "valor_adjudicacion"].sum() > 0 else 0
    max_competencia = df.groupby("nivel_competencia")["id_proceso"].count().idxmax()

    st.markdown(f"""
    * **Eficiencia Global:** El ahorro promedio obtenido sobre el valor total adjudicado es del **{avg_ahorro:.2%}**. 
      * *Interpretación:* Si este porcentaje es bajo, sugiere que los precios base están muy ajustados al valor real del mercado.
    * **Perfil de Competencia:** El nivel de competencia predominante es **{max_competencia}**.
      * *Interpretación:* Esto indica la facilidad de entrada de nuevos proveedores al sistema. Un dominio de nivel 'Bajo' podría sugerir barreras de entrada técnicas o logísticas.
    * **Relación Presupuesto-Adjudicación:** La correlación observada entre precio base y valor adjudicado muestra una tendencia a la {'optimización' if avg_ahorro > 0.05 else 'estabilidad'} presupuestal.
    """)

    # --- 4. Correlación ---
    st.subheader("Mapa de Relación Presupuestal")
    fig_scat = px.scatter(
        df, x="precio_base", y="valor_adjudicacion", color="nivel_competencia",
        title="Dispersión: Precio Base vs Adjudicación (por nivel de competencia)",
        opacity=0.6, log_x=True, log_y=True
    )
    st.plotly_chart(fig_scat, use_container_width=True)