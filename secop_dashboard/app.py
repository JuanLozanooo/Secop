import streamlit as st
from db import test_connection

st.set_page_config(
    page_title="SECOP Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Sistema de Información y Monitoreo SECOP")

with st.sidebar:
    st.header("Estado de conexión")
    try:
        test_connection()
        st.success("Conectado a la base de datos (Supabase)")
    except Exception as e:
        st.error("No se pudo conectar")
        st.caption(str(e))

    st.divider()
    st.subheader("Secciones")
    st.page_link("pages/1_Dashboard.py", label="📌 Dashboard Principal")
    st.page_link("pages/2_Estadisticas.py", label="📈 Estadísticas Avanzadas")
    st.page_link("pages/3_Consultar.py", label="🔎 Consultar Registros")
    st.page_link("pages/4_Agregar.py", label="➕ Agregar Registro")
    st.page_link("pages/5_Tendencias.py", label="📉 Análisis Predictivo y Tendencias")

# Documentación e Introducción del Proyecto
st.markdown(
    """
    ### 🚀 Introducción del Proyecto
    Este sistema interactivo conecta una base de datos relacional de **SECOP** alojada en **Supabase** con una interfaz desarrollada en **Streamlit**, diseñada específicamente para la exploración, auditoría y análisis estratégico de la contratación pública. El objetivo principal es transformar datos abiertos masivos en información estructurada que facilite la toma de decisiones organizacionales.

    ### ⚙️ Ingeniería de Datos y Ciclo de Vida del Dataset
    Para garantizar el rendimiento de la aplicación y la confiabilidad de los análisis, se ejecutó un flujo completo de extracción, transformación y carga (ETL):

    1. **Extracción y Filtrado:** Los datos originales se extrajeron del portal oficial de Datos Abiertos. Mediante la aplicación de filtros selectivos orientados a los objetivos del análisis, se consolidó un dataset optimizado de aproximadamente **200,000 registros**.
    2. **Limpieza y Normalización (Google Colab):** Utilizando entornos de Jupyter Notebooks y la librería **Pandas**, se depuraron todas aquellas variables irrelevantes o redundantes. El proceso de saneamiento incluyó:
        * **Campos de Texto:** Eliminación de espacios en blanco redundantes y caracteres especiales en nombres de entidades, ciudades y departamentos para evitar duplicidades tipográficas.
        * **Campos Temporales:** Transformación de fechas a tipos nativos cronológicos, abstrayendo de manera directa las columnas de *año*, *mes* y *trimestre* para asegurar un agrupamiento histórico libre de registros nulos (`NaT`).
        * **Campos Numéricos:** Formateo estricto de valores financieros, presupuestos base y métricas de participación a variables decimales y enteras de alta precisión.

    3. **Esquema de Datos Estructurado:** El modelo final de la tabla quedó normalizado bajo las siguientes 26 columnas clave:
       `id_proceso`, `entidad`, `nit_entidad`, `departamento`, `ciudad`, `tipo_entidad`, `fecha_publicacion`, `anio`, `mes`, `trimestre`, `modalidad_contratacion`, `tipo_contrato`, `subtipo_contrato`, `categoria_compra`, `duracion_dias`, `proveedores_invitados`, `proveedores_interesados`, `ofertas_recibidas`, `proveedores_unicos`, `precio_base`, `valor_adjudicacion`, `ahorro_obtenido`, `porcentaje_ejecucion`, `nivel_competencia`, `estado_proceso`, `adjudicado`.

    ### 🗄️ Arquitectura, Repositorio y Despliegue
    * **Persistencia en la Nube (Supabase):** El archivo CSV normalizado se migró hacia una instancia remota de PostgreSQL en Supabase, lo que permite realizar operaciones de agregación y filtros complejos del lado del servidor de manera eficiente mediante SQLAlchemy.
    * **Control de Versiones (GitHub):** Todo el entorno de desarrollo, módulos lógicos de consulta (`queries.py`) y formateadores de interfaz (`formatters.py`) se centralizaron en un repositorio de GitHub para asegurar la mantenibilidad del código.
    * **Despliegue Continuo (Streamlit Cloud):** La aplicación web se encuentra completamente desplegada e integrada al repositorio, permitiendo el acceso remoto e interactivo a las herramientas analíticas desde cualquier dispositivo.

    ### 🛠️ Capacidades de las Secciones
    * **📌 Dashboard Principal:** Monitoreo instantáneo de KPIs macro (totales adjudicados, promedios presupuestales) y visualizaciones dinámicas del comportamiento del mercado por año de publicación y áreas geográficas.
    * **📈 Estadísticas Avanzadas:** Desglose analítico de la participación contractual según el nivel de competencia de los oferentes, tipos de contrato y modalidades más recurrentes.
    * **🔎 Consultar Registros:** Motor de búsqueda parametrizado con paginación optimizada para navegar de manera fluida entre los miles de filas del dataset sin degradar la memoria del servidor.
    * **➕ Agregar Registro:** Formulario estructurado para la inserción directa de nuevos procesos contractuales respetando los tipos de datos del esquema PostgreSQL.
    * **📉 Análisis Predictivo y Tendencias:** Evaluación matemática del mercado a través de medias móviles históricas y correlaciones entre presupuestos base y adjudicaciones, permitiendo observar la dirección real de la curva de contratación de forma clara y transparente.
    """
)