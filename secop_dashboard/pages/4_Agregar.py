import streamlit as st

from utils.queries import insert_record

st.title("Agregar registro")

st.write("Completa el formulario para insertar un nuevo proceso en la base de datos.")

with st.form("form_agregar", clear_on_submit=True):
    c1, c2 = st.columns(2)

    with c1:
        entidad = st.text_input("Entidad")
        nit_entidad = st.text_input("Nit Entidad")
        departamento_entidad = st.text_input("Departamento Entidad")
        ciudad_entidad = st.text_input("Ciudad Entidad")
        ordenentidad = st.text_input("OrdenEntidad")
        fecha_pub = st.text_input("Fecha de Publicacion del Proceso")
        precio_base = st.text_input("Precio Base")
        modalidad = st.text_input("Modalidad de Contratacion")
        duracion = st.text_input("Duracion")
        unidad_duracion = st.text_input("Unidad de Duracion")
        proveedores_invitados = st.text_input("Proveedores Invitados")

    with c2:
        proveedores_manifestaron = st.text_input("Proveedores que Manifestaron Interes")
        conteo_respuestas = st.text_input("Conteo de Respuestas a Ofertas")
        proveedores_unicos = st.text_input("Proveedores Unicos con Respuestas")
        numero_lotes = st.text_input("Numero de Lotes")
        valor_adjudicacion = st.text_input("Valor Total Adjudicacion")
        codigo_categoria = st.text_input("Codigo Principal de Categoria")
        tipo_contrato = st.text_input("Tipo de Contrato")
        subtipo_contrato = st.text_input("Subtipo de Contrato")
        estado_resumen = st.text_input("Estado Resumen")
        estado_procedimiento = st.text_input("Estado del Procedimiento")
        adjudicado = st.text_input("Adjudicado")

    submitted = st.form_submit_button("Guardar registro")

if submitted:
    record = {
        "Entidad": entidad,
        "Nit Entidad": nit_entidad,
        "Departamento Entidad": departamento_entidad,
        "Ciudad Entidad": ciudad_entidad,
        "OrdenEntidad": ordenentidad,
        "Fecha de Publicacion del Proceso": fecha_pub,
        "Precio Base": precio_base,
        "Modalidad de Contratacion": modalidad,
        "Duracion": duracion,
        "Unidad de Duracion": unidad_duracion,
        "Proveedores Invitados": proveedores_invitados,
        "Proveedores que Manifestaron Interes": proveedores_manifestaron,
        "Conteo de Respuestas a Ofertas": conteo_respuestas,
        "Proveedores Unicos con Respuestas": proveedores_unicos,
        "Numero de Lotes": numero_lotes,
        "Valor Total Adjudicacion": valor_adjudicacion,
        "Codigo Principal de Categoria": codigo_categoria,
        "Tipo de Contrato": tipo_contrato,
        "Subtipo de Contrato": subtipo_contrato,
        "Estado Resumen": estado_resumen,
        "Estado del Procedimiento": estado_procedimiento,
        "Adjudicado": adjudicado,
    }

    try:
        insert_record(record)
        st.success("Registro guardado correctamente.")
        st.cache_data.clear()
    except Exception as e:
        st.error("No se pudo guardar el registro.")
        st.exception(e)
