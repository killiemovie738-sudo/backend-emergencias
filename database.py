import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Aquí ponemos la dirección de nuestra bodega (PostgreSQL)
# Cambia "tu_usuario" y "tu_contraseña" por los de tu PostgreSQL.
URL_BASE_DATOS = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost/emergencia_db")
URL_BASE_DATOS_FALLBACK = os.getenv("DATABASE_URL_SQLITE", "sqlite:///./emergencia.db")

def crear_engine(url: str):
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url)


# 2. Creamos el motor que hará viajar los datos
try:
    engine = crear_engine(URL_BASE_DATOS)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
except Exception:
    engine = crear_engine(URL_BASE_DATOS_FALLBACK)

# 3. Creamos la sesión (es como abrir la puerta para meter o sacar datos)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Esta es la base mágica con la que crearemos nuestras tablas (Cliente, Taller, etc.)
Base = declarative_base()

# 5. Función para que el mesero pida la llave de la bodega y la devuelva al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()