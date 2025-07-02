import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from routes import (
    user, proyectos, utils
)

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL_VERCEL"), #para produccion
    "http://localhost:5173" #para desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ruta del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="add any string...")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# rutas
app.include_router(user.router)
app.include_router(proyectos.router, prefix="/proyectos", tags=["proyectos"])
app.include_router(utils.router, tags=["utils"])
# app.include_router(ranking.router, prefix="/ranking", tags=["ranking"])
# app.include_router(archivos_proyectos) #da problemas
# app.include_router(postulacion.router, prefix="postulaciones", tags=["postulacion"]) # no implementado