import streamlit as st
from db import test_connection

st.set_page_config(
    page_title="SECOP Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Sistema de Información SECOP")
st.write(
    "Este proyecto conecta tu base de datos de SECOP en Supabase con una app de Streamlit "
    "para consultar, analizar, insertar y visualizar información estratégica."
)

with st.sidebar:
    st.header("Estado de conexión")
    try:
        test_connection()
        st.success("Conectado a la base de datos")
    except Exception as e:
        st.error("No se pudo conectar")
        st.caption(str(e))

    st.divider()
    st.subheader("Secciones")
    st.page_link("pages/1_Dashboard.py", label="📌 Dashboard")
    st.page_link("pages/2_Estadisticas.py", label="📈 Estadísticas")
    st.page_link("pages/3_Consultar.py", label="🔎 Consultar registros")
    st.page_link("pages/4_Agregar.py", label="➕ Agregar registro")
    st.page_link("pages/5_Predicciones.py", label="🤖 Predicciones")

st.subheader("Cómo usar la app")
st.markdown(
    """
1. Verifica que `DATABASE_URL` esté configurado en `.streamlit/secrets.toml`.
2. Entra al dashboard para ver KPIs y gráficos.
3. Usa la sección de consulta para filtrar registros.
4. Agrega nuevos datos desde el formulario.
5. Revisa el módulo de predicciones para un modelo exploratorio.

**Nota:** La app está diseñada para una tabla grande, así que las consultas principales se hacen con agregaciones y paginación.
"""
)

st.info("Si quieres publicar esta app en Streamlit Cloud, sube este proyecto a GitHub y agrega los secretos en el panel de despliegue.")
