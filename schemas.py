from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LibroBase(BaseModel):
    """
    Esquema base con los campos comunes de un libro.
    Se reutiliza para creación, actualización y lectura.
    """

    # Título obligatorio, mínimo 1 carácter y máximo 150
    titulo: str = Field(
        min_length=1,
        max_length=150,
        description="Título del libro",
    )

    # Autor obligatorio, mínimo 1 carácter y máximo 150
    autor: str = Field(
        min_length=1,
        max_length=150,
        description="Autor del libro",
    )

    # Rating obligatorio entre 1 y 5
    rating: int = Field(
        ge=1,
        le=5,
        description="Valoración del libro entre 1 y 5",
    )


class LibroCreate(LibroBase):
    """
    Esquema usado para crear libros.
    Hereda todos los campos obligatorios de LibroBase.
    """

    pass


class LibroUpdate(BaseModel):
    """
    Esquema usado para actualizar libros.

    Los campos son opcionales para permitir actualizaciones parciales.
    Por ejemplo, podrías cambiar solo el rating sin enviar título y autor.
    """

    titulo: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150,
        description="Nuevo título del libro",
    )

    autor: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150,
        description="Nuevo autor del libro",
    )

    rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="Nueva valoración del libro entre 1 y 5",
    )


class LibroRead(LibroBase):
    """
    Esquema usado para responder datos desde la API.

    Incluye el id porque ese dato lo genera la base de datos.
    """

    id: int

    # Configuración moderna de Pydantic v2.
    # Permite convertir objetos SQLAlchemy a respuestas Pydantic.
    model_config = ConfigDict(from_attributes=True)