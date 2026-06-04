import plotly.express as px
import streamlit as st

from utils.queries import get_top_counts, get_top_values

st.title("Estadísticas avanzadas")

st.write("Esta vista muestra resúmenes adicionales para apoyar la toma de decisiones estratégicas.")

c1, c2 = st.columns(2)

with c1:
    df_estado = get_top_counts("estado_proceso", 10)
    if not df_estado.empty:
        fig = px.pie(df_estado, names="label", values="value", title="Distribución por estado de proceso")
        st.plotly_chart(fig, use_container_width=True)

with c2:
    df_proc = get_top_counts("nivel_competencia", 10)
    if not df_proc.empty:
        fig = px.pie(df_proc, names="label", values="value", title="Distribución por nivel de competencia")
        st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    df_val_tipo = get_top_values("tipo_contrato", "valor_adjudicacion", 10)
    if not df_val_tipo.empty:
        fig = px.bar(df_val_tipo, x="label", y="value", title="Valor adjudicado por tipo de contrato")
        fig.update_layout(xaxis_title="", yaxis_title="Valor adjudicado")
        st.plotly_chart(fig, use_container_width=True)

with c4:
    df_val_modalidad = get_top_values("modalidad_contratacion", "valor_adjudicacion", 10)
    if not df_val_modalidad.empty:
        fig = px.bar(df_val_modalidad, x="label", y="value", title="Valor adjudicado por modalidad")
        fig.update_layout(xaxis_title="", yaxis_title="Valor adjudicado")
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Top entidades por número de procesos")
df_ent = get_top_counts("entidad", 15)
st.dataframe(df_ent, use_container_width=True, hide_index=True)

st.subheader("Top ciudades por número de procesos")
df_city = get_top_counts("ciudad", 15)
st.dataframe(df_city, use_container_width=True, hide_index=True)

st.subheader("Top categorías por valor adjudicado")
df_cat_val = get_top_values("categoria_compra", "valor_adjudicacion", 15)
st.dataframe(df_cat_val, use_container_width=True, hide_index=True)