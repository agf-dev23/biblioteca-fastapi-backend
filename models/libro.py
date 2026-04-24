from sqlalchemy import Column, Integer, String

from database import Base


class Libro(Base):
    # Nombre real de la tabla en MySQL
    __tablename__ = "libros"

    # Llave primaria autoincremental
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Título del libro, obligatorio
    titulo = Column(String(150), nullable=False)

    # Autor del libro, obligatorio
    autor = Column(String(150), nullable=False)

    # Rating del libro, obligatorio
    # La validación 1-5 la reforzaremos también con Pydantic en fases posteriores
    rating = Column(Integer, nullable=False)