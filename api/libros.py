from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import LibroCreate, LibroRead, LibroUpdate
from services.libro_service import (
    actualizar_libro,
    crear_libro,
    eliminar_libro,  # [NUEVO]
    listar_libros,
    obtener_libro_por_id,
)


# Creamos un router específico para las rutas de libros.
router = APIRouter(
    prefix="/api/libros",
    tags=["Libros"],
)


# Endpoint para listar todos los libros.
@router.get("/", response_model=List[LibroRead])
def obtener_libros(db: Session = Depends(get_db)):
    return listar_libros(db)


# Endpoint para crear un nuevo libro.
@router.post(
    "/",
    response_model=LibroRead,
    status_code=status.HTTP_201_CREATED,
)
def agregar_libro(datos: LibroCreate, db: Session = Depends(get_db)):
    return crear_libro(db, datos)


# Endpoint para obtener un libro por id.
@router.get("/{id}", response_model=LibroRead)
def obtener_libro(
    id: int = Path(gt=0, description="ID del libro a consultar"),
    db: Session = Depends(get_db),
):
    libro = obtener_libro_por_id(db, id)

    if libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado",
        )

    return libro


# Endpoint para actualizar un libro existente.
@router.put("/{id}", response_model=LibroRead)
def editar_libro(
    datos: LibroUpdate,
    id: int = Path(gt=0, description="ID del libro a actualizar"),
    db: Session = Depends(get_db),
):
    libro_actualizado = actualizar_libro(db, id, datos)

    if libro_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado",
        )

    return libro_actualizado


# [NUEVO] Endpoint para eliminar un libro existente.
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def borrar_libro(
    id: int = Path(gt=0, description="ID del libro a eliminar"),
    db: Session = Depends(get_db),
):
    # Intentamos eliminar el libro usando la capa de servicios
    libro_eliminado = eliminar_libro(db, id)

    # Si no existe, devolvemos 404
    if libro_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado",
        )

    return {
        "mensaje": "Libro eliminado correctamente",
        "id": id,
    }