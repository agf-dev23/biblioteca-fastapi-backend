from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # [NUEVO]

from api.libros import router as libros_router


# Creamos la instancia principal de FastAPI
app = FastAPI(
    title="Biblioteca Personal API",
    description="API REST para administrar libros personales.",
    version="1.0.0",
)


# [NUEVO] Configuración de CORS
origins = [
    "http://localhost:4200",  # Angular
    "http://localhost:5173",  # React (Vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos los headers
)


# Registramos el router de libros
app.include_router(libros_router)


# Endpoint de prueba
@app.get("/")
def inicio():
    return {
        "mensaje": "API de Biblioteca Personal funcionando correctamente 📚"
    }