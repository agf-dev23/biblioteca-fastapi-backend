from sqlalchemy.orm import Session

from models.libro import Libro
from schemas import LibroCreate, LibroUpdate


# Función para listar todos los libros
def listar_libros(db: Session):
    """
    Obtiene todos los registros de la tabla 'libros'.
    """
    libros = db.query(Libro).all()
    return libros


# Función para crear un nuevo libro
def crear_libro(db: Session, datos: LibroCreate):
    """
    Crea un nuevo registro en la tabla 'libros'.
    """
    nuevo_libro = Libro(
        titulo=datos.titulo,
        autor=datos.autor,
        rating=datos.rating,
    )

    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)

    return nuevo_libro


# Función para obtener un libro por su ID
def obtener_libro_por_id(db: Session, id: int):
    """
    Busca un libro por su id.
    """
    libro = db.query(Libro).filter(Libro.id == id).first()
    return libro


# Función para actualizar un libro existente
def actualizar_libro(db: Session, id: int, datos: LibroUpdate):
    """
    Actualiza un libro existente.

    Si el libro no existe, devuelve None.
    Si existe, aplica solo los campos enviados.
    """
    libro = obtener_libro_por_id(db, id)

    if libro is None:
        return None

    datos_actualizados = datos.model_dump(exclude_unset=True)

    for campo, valor in datos_actualizados.items():
        setattr(libro, campo, valor)

    db.commit()
    db.refresh(libro)

    return libro


# [NUEVO] Función para eliminar un libro existente
def eliminar_libro(db: Session, id: int):
    """
    Elimina físicamente un libro de la base de datos.

    Si el libro no existe, devuelve None.
    Si existe, lo elimina y devuelve el libro eliminado.
    """

    # Buscamos primero el libro por id
    libro = obtener_libro_por_id(db, id)

    # Si no existe, devolvemos None
    if libro is None:
        return None

    # Eliminamos el libro de la sesión
    db.delete(libro)

    # Confirmamos el borrado en MySQL
    db.commit()

    return libro