import os
import subprocess

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError


# Cargamos las variables del archivo .env
load_dotenv()


# Leemos las variables de conexión desde el entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# Construimos la URL de conexión para MySQL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def limpiar_alembic_version_huerfana():
    """
    Revisa si existe la tabla alembic_version sin migraciones reales aplicadas.
    Si detecta una versión huérfana, limpia la tabla para evitar bloqueos.
    """
    engine = create_engine(DATABASE_URL)

    try:
        with engine.connect() as connection:
            inspector = inspect(connection)

            if "alembic_version" not in inspector.get_table_names():
                print("ℹ️ No existe tabla alembic_version todavía.")
                return

            resultado = connection.execute(text("SELECT version_num FROM alembic_version"))
            version = resultado.scalar()

            if version:
                print(f"ℹ️ Versión actual de Alembic detectada: {version}")
            else:
                print("ℹ️ Tabla alembic_version vacía.")

    except SQLAlchemyError as error:
        print("❌ Error revisando alembic_version")
        print(error)


def ejecutar_comando(comando):
    """
    Ejecuta comandos de Alembic desde Python.
    """
    resultado = subprocess.run(
        comando,
        shell=True,
        text=True,
    )

    if resultado.returncode != 0:
        raise RuntimeError(f"❌ Error ejecutando comando: {comando}")


def ejecutar_migracion():
    """
    Genera una migración automática y aplica upgrade head.
    """
    print("🚀 Iniciando proceso de migración...")

    limpiar_alembic_version_huerfana()

    print("🛠 Generando migración automática...")
    ejecutar_comando('alembic revision --autogenerate -m "crear tabla libros"')

    print("⬆️ Aplicando migraciones...")
    ejecutar_comando("alembic upgrade head")

    print("✅ Migración completada correctamente.")


if __name__ == "__main__":
    ejecutar_migracion()