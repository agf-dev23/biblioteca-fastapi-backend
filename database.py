import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

# Cargamos las variables del archivo .env
load_dotenv()

# Leemos las variables de conexión desde el entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construimos la URL de conexión para MySQL usando PyMySQL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Creamos el motor de conexión de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Creamos una fábrica de sesiones para trabajar con la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base será la clase padre para nuestros modelos SQLAlchemy
Base = declarative_base()


# Dependencia para FastAPI.
# Abre una sesión de base de datos por petición y la cierra al finalizar.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Prueba rápida de conexión.
# Permite ejecutar: python database.py
if __name__ == "__main__":
    try:
        with engine.connect():
            print("✅ Conexión exitosa a MySQL")
    except SQLAlchemyError as error:
        print("❌ Error al conectar con MySQL")
        print(error)