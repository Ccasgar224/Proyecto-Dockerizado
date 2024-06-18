
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from config import SQLALCHEMY_DATABASE_URI

# Configura la URI de la base de datos
DB_URL = SQLALCHEMY_DATABASE_URI

# Crea una instancia de SQLAlchemy
db = SQLAlchemy()
engine = create_engine(DB_URL) #Motor de la base de datos

# Crear el scoped_session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine)) #Sesión de la base de datos
metadata = MetaData()

#Devuelve la sesion de la base de datos
def session_factory():
    return db.session

#Carga la estructura de la base de datos en metadata
def init_db():
    metadata.reflect(bind=engine)

# Cerrar la sesión
def cierra_sesion(exception=None):
    db_session.remove()



