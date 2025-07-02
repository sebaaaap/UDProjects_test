from sqlalchemy import Column, Integer, String
from db.database import Base

class CorreoProfesor(Base):
    __tablename__ = "correo_profesores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    correo = Column(String, unique=True, nullable=False)