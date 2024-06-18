from flask import Flask, render_template, redirect, url_for, flash, Blueprint, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_swagger_ui import get_swaggerui_blueprint
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from database import db_session, init_db
from generate_api import guardar_specs_swagger
from routes import crea_rutas
from forms import FormularioLogin, FormularioRegistro
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'my_default_secret_key')
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY

# Inicializar las extensiones Flask
jwt = JWTManager(app)
api = Api(app)
db = SQLAlchemy(app)

# Inicializar la base de datos
init_db()

# Definir el blueprint para la API
blueprint = Blueprint('api', __name__)

# Crear rutas dinámicas basadas en la estructura de la base de datos
crea_rutas(app, db_session)

# Generar y guardar la especificación Swagger
guardar_specs_swagger(app, db_session)

# Definición del modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))

# Crear la base de datos y las tablas
@app.before_first_request
def create_tables():
    db.create_all()

# Errores flash
def flash_errors(form):
    for field, errors in form.errors.items(): #Itera dobre el diccionario form.items 
        for error in errors: # Para cada campo itera sobre la lista de errores
            flash(f'{getattr(form, field).label.text}: {error}', 'danger') #Obtiene el objeto del campo con el texto y construye el mensaje de error

# Ruta para el registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.query.filter_by(email=form.email.data).first() #Comprueba que el email que ha intentado registrar existe o no
            if existing_user:
                flash('Este correo electrónico ya está en uso.', 'danger')
            else:
                try:
                    hashed_password = generate_password_hash(form.password.data) #Cifra la contraseña 
                    new_user = User(nombre=form.nombre.data, email=form.email.data, password=hashed_password) #Crea un nuevo objeto User
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Registrado con éxito!', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    db.session.rollback()
                    flash('Error al registrar: {}'.format(str(e)), 'danger')
        else:
            flash_errors(form)
    return render_template('registro.html', form=form)

# Ruta para el login
@app.route('/', methods=['GET', 'POST'])
def login():
    form = FormularioLogin()
    if request.method == 'POST':  
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                access_token = create_access_token(identity={'email': user.email, 'name': user.nombre})
                return jsonify(access_token=access_token), 200
            else:
                flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)


@app.route('/index')
@jwt_required(optional=True)
def index():
    current_user = get_jwt_identity()
    user_name = current_user.get('name') if current_user else None
    metadata = MetaData() #Clase de SQLAlchemy que representa la estructura de la base de datos
    metadata.reflect(bind=db_session.bind) # "Llena" el objeto metadata con las tablas de la BD que está conectada a db_session
    tables = [table_name for table_name in metadata.tables.keys() if table_name != 'user']  # filtrar las tablas y omitir 'User'
    return render_template('index.html', current_user=user_name, tables=tables)

# Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API generada automáticamente"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#Asegura que solo se ejecute la app si esta script se ejecuta directamente e inicia la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
