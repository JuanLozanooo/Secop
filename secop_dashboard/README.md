# SECOP Dashboard

Aplicación de Streamlit para analizar procesos de contratación SECOP conectada a Supabase/PostgreSQL.

## Qué hace
- Conecta la tabla `secop`
- Muestra KPIs y gráficos
- Permite consultar registros con filtros y paginación
- Permite agregar nuevos registros
- Incluye un módulo de predicción exploratoria
- Descarga CSV de la consulta actual

## Requisito principal
Debes definir `DATABASE_URL` en `.streamlit/secrets.toml`.

Ejemplo:

```toml
DATABASE_URL="postgresql+psycopg2://postgres:TU_PASSWORD@db.TU_PROJECT_REF.supabase.co:5432/postgres?sslmode=require"
```

## Estructura
```text
secop_dashboard/
├── app.py
├── db.py
├── requirements.txt
├── pages/
└── utils/
```

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Cloud
1. Sube el proyecto a GitHub.
2. Conecta el repositorio en Streamlit Cloud.
3. Agrega `DATABASE_URL` en los secretos del deploy.
4. Usa `app.py` como archivo principal.
