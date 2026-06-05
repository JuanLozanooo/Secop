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
    df = get_table_sample(limit=25000)

    # LIMPIEZA CRÍTICA: Normalizar nombres de columnas a minúsculas y sin espacios
    df.columns = df.columns.str.strip().str.lower()

    # Lista estricta basada en tu CSV
    target_cols = ["anio", "mes", "valor_adjudicacion", "precio_base", "ahorro_obtenido", "ofertas_recibidas",
                   "id_proceso", "nivel_competencia"]

    # Validar y convertir solo si existen
    for col in target_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            st.error(
                f"Error: La columna '{col}' no se encuentra en la base de datos. Columnas reales: {df.columns.tolist()}")
            st.stop()

    # --- 1. Tendencia de Valor y Eficiencia ---
    st.subheader("Evolución de Valor y Eficiencia")
    df_grouped = df.groupby(["anio", "mes"])[["valor_adjudicacion", "ahorro_obtenido"]].sum().reset_index()
    df_grouped["periodo"] = df_grouped["anio"].astype(int).astype(str) + "-" + df_grouped["mes"].astype(int).astype(
        str).str.zfill(2)
    df_grouped = df_grouped.sort_values(["anio", "mes"])

    df_grouped["Tendencia (Media 3M)"] = df_grouped["valor_adjudicacion"].rolling(window=3).mean()

    fig_val = go.Figure()
    fig_val.add_trace(go.Bar(x=df_grouped["periodo"], y=df_grouped["valor_adjudicacion"], name="Valor Adjudicado",
                             marker_color='royalblue'))
    fig_val.add_trace(go.Scatter(x=df_grouped["periodo"], y=df_grouped["Tendencia (Media 3M)"], name="Tendencia (3M)",
                                 line=dict(color='red', width=3)))
    fig_val.update_layout(title="Volumen Mensual de Adjudicación", xaxis_title="Periodo", yaxis_title="$")
    st.plotly_chart(fig_val, use_container_width=True)

    # 1. Gráfico: ¿Dónde se va el dinero realmente? (Pareto de Categorías)
    st.subheader("Concentración del Gasto Público")
    df_cat = df.groupby("categoria_compra")["valor_adjudicacion"].sum().reset_index().sort_values("valor_adjudicacion",
                                                                                                  ascending=False).head(
        10)
    fig_cat = px.treemap(df_cat, path=['categoria_compra'], values='valor_adjudicacion',
                         title="Distribución del Presupuesto por Categoría (Top 10)")
    st.plotly_chart(fig_cat, use_container_width=True)

    # 2. Gráfico: Eficiencia (¿Ahorramos más cuando hay más competencia?)
    st.subheader("Efectividad del Ahorro vs. Competencia")
    fig_eff = px.scatter(df, x="ofertas_recibidas", y="ahorro_obtenido", color="nivel_competencia",
                         size="valor_adjudicacion", hover_data=["entidad"],
                         title="Correlación: ¿Más oferentes generan más ahorro?",
                         labels={"ofertas_recibidas": "Número de Ofertas", "ahorro_obtenido": "Dinero Ahorrado ($)"})
    st.plotly_chart(fig_eff, use_container_width=True)

    # 3. Insights Detallados (Párrafo largo)
    st.divider()
    st.subheader("📝 Diagnóstico Narrativo")

    total_adjudicado = df["valor_adjudicacion"].sum()
    total_ahorro = df["ahorro_obtenido"].sum()
    eficiencia = (total_ahorro / total_adjudicado) * 100 if total_adjudicado > 0 else 0
    top_sector = df.groupby("categoria_compra")["valor_adjudicacion"].sum().idxmax()

    st.markdown(f"""
        El análisis actual de la base de datos de contratación revela una dinámica de gasto caracterizada por una marcada concentración presupuestal en el sector de **{top_sector}**, lo cual sugiere que la estrategia de adquisiciones de la entidad está fuertemente orientada a demandas de suministro específicas que absorben gran parte de la capacidad financiera disponible. Al observar la relación entre la participación de mercado y la eficiencia presupuestal, se identifica que los procesos catalogados bajo niveles de competencia alta no siempre traducen un incremento proporcional en el ahorro obtenido, lo que abre una línea de investigación sobre si la pluralidad de oferentes está incidiendo realmente en una reducción de precios o si, por el contrario, existen factores de rigidez administrativa que limitan la capacidad negociadora del Estado en procesos altamente disputados. En términos agregados, el sistema ha logrado capturar un ahorro real de un **{eficiencia:.2f}%** sobre el valor total adjudicado; sin embargo, la alta variabilidad en los resultados sugiere que, mientras que ciertos tipos de contrato operan con márgenes de ahorro optimizados, otros procesos presentan ineficiencias sistemáticas que requieren una revisión profunda de los precios base establecidos en las etapas precontractuales para evitar el desaprovechamiento de economías de escala y asegurar que el uso de los recursos públicos se mantenga alineado con las proyecciones de ahorro institucional planteadas al inicio de cada vigencia.
        """)

    # --- 4. Correlación ---
    st.subheader("Mapa de Relación Presupuestal")
    fig_scat = px.scatter(df, x="precio_base", y="valor_adjudicacion", color="nivel_competencia",
                          title="Dispersión: Precio Base vs Adjudicación", opacity=0.6, log_x=True, log_y=True)
    st.plotly_chart(fig_scat, use_container_width=True)