import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

# Cargamos variables locales desde .env
load_dotenv()

# Leemos variables del entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Validamos que Railway/local tenga todas las variables necesarias
required_vars = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
}

# Si falta alguna variable, mostramos exactamente cuál falta
missing_vars = [name for name, value in required_vars.items() if not value]

if missing_vars:
    raise RuntimeError(
        f"Faltan variables de entorno para la base de datos: {', '.join(missing_vars)}"
    )

# Construimos la URL de conexión MySQL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Creamos el motor de conexión
engine = create_engine(DATABASE_URL)

# Creamos sesiones para usar en FastAPI
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Clase base para los modelos
Base = declarative_base()


# Dependencia para abrir/cerrar conexión por cada petición
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Prueba rápida ejecutando: python database.py
if __name__ == "__main__":
    try:
        with engine.connect():
            print("✅ Conexión exitosa a MySQL")
    except SQLAlchemyError as error:
        print("❌ Error al conectar con MySQL")
        print(error)