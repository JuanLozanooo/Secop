import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from utils.queries import get_table_sample

st.title("Predicciones exploratorias")

st.write(
    "Este módulo entrena un modelo simple sobre una muestra de la base para estimar el valor total de adjudicación."
)


def _to_num(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()

    s = (
        s.str.replace("$", "", regex=False)
         .str.replace(" ", "", regex=False)
         .str.replace(".", "", regex=False)
         .str.replace(",", ".", regex=False)
    )

    return pd.to_numeric(s, errors="coerce")

if st.button("Entrenar modelo"):
    df = get_table_sample(limit=15000)
    st.write("Columnas encontradas:")
    st.write(df.columns.tolist())

    numeric_cols = [
        "Precio Base",
        "Duracion",
        "Proveedores Invitados",
        "Proveedores que Manifestaron Interes",
        "Conteo de Respuestas a Ofertas",
        "Proveedores Unicos con Respuestas",
        "Numero de Lotes",
        "Valor Total Adjudicacion",
    ]
    cat_cols = [
        "Modalidad de Contratacion",
        "Tipo de Contrato",
        "Departamento Entidad",
        "Ciudad Entidad",
        "Estado Resumen",
        "Adjudicado",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = _to_num(df[col])
        else:
            st.error(f"No existe la columna: {col}")
            st.stop()

    df = df.dropna(subset=["Valor Total Adjudicacion"])
    if len(df) < 100:
        st.warning("No hay suficientes datos limpios para entrenar el modelo.")
        st.stop()

    feature_cols = [c for c in numeric_cols if c != "Valor Total Adjudicacion"] + cat_cols
    X = df[feature_cols]
    y = df["Valor Total Adjudicacion"]

    numeric_features = [c for c in feature_cols if c not in cat_cols]
    categorical_features = cat_cols

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]), numeric_features),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        max_depth=12,
    )

    pipe = Pipeline(steps=[("prep", preprocessor), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)

    mse = mean_squared_error(y_test, pred)
    rmse = mse ** 0.5
    mae = mean_absolute_error(y_test, pred)
    r2 = r2_score(y_test, pred)

    c1, c2, c3 = st.columns(3)
    c1.metric("RMSE", f"{rmse:,.2f}")
    c2.metric("MAE", f"{mae:,.2f}")
    c3.metric("R²", f"{r2:.3f}")

    st.success("Modelo entrenado sobre una muestra de la tabla.")

    st.subheader("Probar una predicción")

    with st.form("predict_form"):
        p1, p2 = st.columns(2)
        with p1:
            precio_base = st.text_input("Precio Base", value="0")
            duracion = st.text_input("Duracion", value="0")
            proveedores_invitados = st.text_input("Proveedores Invitados", value="0")
            proveedores_manifestaron = st.text_input("Proveedores que Manifestaron Interes", value="0")
        with p2:
            conteo_respuestas = st.text_input("Conteo de Respuestas a Ofertas", value="0")
            proveedores_unicos = st.text_input("Proveedores Unicos con Respuestas", value="0")
            numero_lotes = st.text_input("Numero de Lotes", value="0")
            modalidad = st.text_input("Modalidad de Contratacion", value="")
        tipo = st.text_input("Tipo de Contrato", value="")
        depto = st.text_input("Departamento Entidad", value="")
        ciudad = st.text_input("Ciudad Entidad", value="")
        estado = st.text_input("Estado Resumen", value="")
        adjudicado = st.text_input("Adjudicado", value="")

        run_pred = st.form_submit_button("Predecir")

    if run_pred:
        sample = pd.DataFrame(
            [{
                "Precio Base": precio_base,
                "Duracion": duracion,
                "Proveedores Invitados": proveedores_invitados,
                "Proveedores que Manifestaron Interes": proveedores_manifestaron,
                "Conteo de Respuestas a Ofertas": conteo_respuestas,
                "Proveedores Unicos con Respuestas": proveedores_unicos,
                "Numero de Lotes": numero_lotes,
                "Modalidad de Contratacion": modalidad,
                "Tipo de Contrato": tipo,
                "Departamento Entidad": depto,
                "Ciudad Entidad": ciudad,
                "Estado Resumen": estado,
                "Adjudicado": adjudicado,
            }]
        )

        for col in numeric_features:
            if col in sample.columns:
                sample[col] = _to_num(sample[col])

        prediction = pipe.predict(sample[feature_cols])[0]
        st.metric("Valor Total Adjudicación estimado", f"{prediction:,.2f}")
