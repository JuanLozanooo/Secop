import streamlit as st

from utils.queries import insert_record

st.title("Agregar registro")

st.write("Completa el formulario para insertar un nuevo proceso en la base de datos.")

with st.form("form_agregar", clear_on_submit=True):
    c1, c2 = st.columns(2)

    with c1:
        id_proceso = st.text_input("ID Proceso")
        entidad = st.text_input("Entidad")
        nit_entidad = st.text_input("NIT Entidad")
        departamento = st.text_input("Departamento")
        ciudad = st.text_input("Ciudad")
        tipo_entidad = st.text_input("Tipo de Entidad (Nacional/Territorial)")
        fecha_publicacion = st.text_input("Fecha de Publicación (YYYY-MM-DD)")
        anio = st.text_input("Año")
        mes = st.text_input("Mes")
        trimestre = st.text_input("Trimestre")
        modalidad_contratacion = st.text_input("Modalidad de Contratación")
        tipo_contrato = st.text_input("Tipo de Contrato")
        subtipo_contrato = st.text_input("Subtipo de Contrato")

    with c2:
        categoria_compra = st.text_input("Categoría de Compra")
        duracion_dias = st.text_input("Duración en Días")
        proveedores_invitados = st.text_input("Proveedores Invitados")
        proveedores_interesados = st.text_input("Proveedores Interesados")
        ofertas_recibidas = st.text_input("Ofertas Recibidas")
        proveedores_unicos = st.text_input("Proveedores Únicos")
        precio_base = st.text_input("Precio Base")
        valor_adjudicacion = st.text_input("Valor Adjudicación")
        ahorro_obtenido = st.text_input("Ahorro Obtenido")
        porcentaje_ejecucion = st.text_input("Porcentaje de Ejecución")
        nivel_competencia = st.text_input("Nivel de Competencia (Alta/Media/Baja)")
        estado_proceso = st.text_input("Estado del Proceso")
        adjudicado = st.text_input("Adjudicado (Si/No)")

    submitted = st.form_submit_button("Guardar registro")

if submitted:
    # Las llaves de este diccionario deben ser EXACTAMENTE las columnas de tu BD
    record = {
        "id_proceso": id_proceso,
        "entidad": entidad,
        "nit_entidad": nit_entidad,
        "departamento": departamento,
        "ciudad": ciudad,
        "tipo_entidad": tipo_entidad,
        "fecha_publicacion": fecha_publicacion,
        "anio": anio,
        "mes": mes,
        "trimestre": trimestre,
        "modalidad_contratacion": modalidad_contratacion,
        "tipo_contrato": tipo_contrato,
        "subtipo_contrato": subtipo_contrato,
        "categoria_compra": categoria_compra,
        "duracion_dias": duracion_dias,
        "proveedores_invitados": proveedores_invitados,
        "proveedores_interesados": proveedores_interesados,
        "ofertas_recibidas": ofertas_recibidas,
        "proveedores_unicos": proveedores_unicos,
        "precio_base": precio_base,
        "valor_adjudicacion": valor_adjudicacion,
        "ahorro_obtenido": ahorro_obtenido,
        "porcentaje_ejecucion": porcentaje_ejecucion,
        "nivel_competencia": nivel_competencia,
        "estado_proceso": estado_proceso,
        "adjudicado": adjudicado
    }

    try:
        insert_record(record)
        st.success("Registro guardado correctamente.")
        st.cache_data.clear()
    except Exception as e:
        st.error("No se pudo guardar el registro.")
        st.exception(e)