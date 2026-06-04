import os
from typing import Optional

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def _secret(key: str, default: Optional[str] = None) -> Optional[str]:
    try:
        value = st.secrets[key]
        return value if value else default
    except Exception:
        return os.getenv(key, default)


@st.cache_resource
def get_engine() -> Engine:
    """
    Crea y reutiliza el engine de SQLAlchemy.
    Espera la variable DATABASE_URL en secrets o variables de entorno.
    """
    database_url = _secret("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "Falta DATABASE_URL. Crea .streamlit/secrets.toml con la cadena de conexión de Supabase."
        )
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        future=True,
    )


def test_connection() -> bool:
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
