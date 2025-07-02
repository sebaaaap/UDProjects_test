from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import user, proyectos, ranking, archivos_proyectos, evaluacion_proyecto, utils

app = FastAPI()

# CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(proyectos.router, prefix="/proyectos")
app.include_router(ranking.router, prefix="/ranking")
app.include_router(archivos_proyectos.router, prefix="/proyectos")
app.include_router(evaluacion_proyecto.router)
app.include_router(utils.router) 