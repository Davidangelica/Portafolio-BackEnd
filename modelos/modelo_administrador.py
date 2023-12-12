# basemodel
from pydantic import BaseModel
#datetime
from datetime import datetime,date
#sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker


class Admin (BaseModel):
    id: int | None
    nombre : str
    apellido : str
    email : str
    nombre_de_usuario : str
    contraseña : str
    fecha_de_creacion : datetime | None
    
    

db_url = 'sqlite:///C:/Users/angel/Desktop/portafolio/base_de_datos.db'
engine = create_engine(db_url)
base = declarative_base()

class AdminDB (base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(100), unique=True)
    nombre_de_usuario = Column(String(50), unique=True)
    contraseña = Column(String(100))
    fecha_de_creacion = Column(DateTime) 
            
base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
sesion_admin = session()