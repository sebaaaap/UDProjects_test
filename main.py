import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from routes import user, proyectos, utils

app = FastAPI()

origins = [
    "http://localhost:5173", #para desarrollo
    os.getenv("FRONTEND_URL") #para produccion
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ruta del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(proyectos.router, prefix="/proyectos", tags=["proyectos"])
app.include_router(utils.router, tags=["utils"])

app.add_middleware(SessionMiddleware, secret_key="add any string...")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# if __name__ == "__main__":
#     uvicorn.run(
#         app="main:app",
#         host="localhost",
#         port=8000,
#         reload=True
#     )