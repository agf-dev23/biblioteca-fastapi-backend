# ==============================
# IMPORTS
# ==============================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.libros import router as libros_router

# 👇 IMPORTS PARA BASE DE DATOS
from database import Base, engine
from models.libro import Libro  # necesario para que detecte la tabla


# ==============================
# APP
# ==============================

app = FastAPI(
    title="Biblioteca Personal API",
    description="API REST para administrar libros personales.",
    version="1.0.0",
)


# ==============================
# CREAR TABLAS AUTOMÁTICAMENTE
# ==============================

# Esto crea la tabla 'libros' en Railway si no existe
Base.metadata.create_all(bind=engine)


# ==============================
# CORS (MUY IMPORTANTE)
# ==============================

origins = [
    "http://localhost:4200",
    "http://localhost:5173",
    "https://biblioteca-react-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# ROUTERS
# ==============================

app.include_router(libros_router)


# ==============================
# ENDPOINT DE PRUEBA
# ==============================

@app.get("/")
def inicio():
    return {
        "mensaje": "API de Biblioteca Personal funcionando correctamente 🚀"
    }