from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.libros import router as libros_router

# 👇 IMPORTS NUEVOS
from database import Base, engine
from models.libro import Libro  # importante para que detecte la tabla


# Creamos la instancia principal de FastAPI
app = FastAPI(
    title="Biblioteca Personal API",
    description="API REST para administrar libros personales.",
    version="1.0.0",
)

# 👇 ESTO ES LA CLAVE
# Crea automáticamente las tablas en MySQL si no existen
Base.metadata.create_all(bind=engine)


# Configuración de CORS
origins = [
    "http://localhost:4200",
    "http://localhost:5173",
    # 👇 añade tu frontend en producción (Vercel)
    "https://TU-FRONTEND.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registramos el router de libros
app.include_router(libros_router)


# Endpoint de prueba
@app.get("/")
def inicio():
    return {
        "mensaje": "API de Biblioteca Personal funcionando correctamente 📚"
    }