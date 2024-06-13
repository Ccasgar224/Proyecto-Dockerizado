import json
import os
from sqlalchemy import MetaData
from database import engine
from routes import crea_rutas

def generar_api(app, db_session, blueprint):
    crea_rutas(app, db_session, blueprint)

def generar_swagger(app, db_session):
    paths = {}
    metadata = MetaData()
    metadata.reflect(bind=engine)

    for table_name in metadata.tables.keys():
        paths[f'/Asignacion/{table_name}'] = {
            'get': {
                'summary': f'Recuperar todos los registros de {table_name}',
                'responses': {
                    '200': {'description': 'Éxito'},
                    '400': {'description': 'Solicitud incorrecta'},
                    '404': {'description': 'No encontrado'}
                }
            },
            'post': {
                'summary': f'Crear un nuevo registro en {table_name}',
                'parameters': [
                    {
                        'name': 'body',
                        'in': 'body',
                        'required': True,
                        'schema': {'type': 'object'}
                    }
                ],
                'responses': {
                    '201': {'description': 'Creado'},
                    '400': {'description': 'Solicitud incorrecta'}
                }
            }
        }

        paths[f'/api/{table_name}/<int:id>'] = {
            'get': {
                'summary': f'Recuperar un registro de {table_name} por ID',
                'responses': {
                    '200': {'description': 'Éxito'},
                    '400': {'description': 'Solicitud incorrecta'},
                    '404': {'description': 'No encontrado'}
                }
            },
            'put': {
                'summary': f'Actualizar un registro en {table_name} por ID',
                'parameters': [
                    {
                        'name': 'body',
                        'in': 'body',
                        'required': True,
                        'schema': {'type': 'object'}
                    }
                ],
                'responses': {
                    '200': {'description': 'Éxito'},
                    '400': {'description': 'Solicitud incorrecta'},
                    '404': {'description': 'No encontrado'}
                }
            },
            'delete': {
                'summary': f'Eliminar un registro de {table_name} por ID',
                'responses': {
                    '200': {'description': 'Éxito'},
                    '400': {'description': 'Solicitud incorrecta'},
                    '404': {'description': 'No encontrado'}
                }
            }
        }

    modelos = {}
    for name, table in metadata.tables.items():
        propiedades = {}
        for column in table.columns:
            tipo_columna = str(column.type)
            formato_propiedad = None  
            if tipo_columna.startswith('VARCHAR'):
                tipo_propiedad = 'string'
            elif tipo_columna.startswith('INTEGER'):
                tipo_propiedad = 'integer'
            elif tipo_columna.startswith('BOOLEAN'):
                tipo_propiedad = 'boolean'
            elif tipo_columna.startswith('DATE'):
                tipo_propiedad = 'string'
                formato_propiedad = 'date'
            else:
                tipo_propiedad = 'string'

            propiedades[column.name] = {'type': tipo_propiedad}
            if formato_propiedad:
                propiedades[column.name]['format'] = formato_propiedad

        modelos[name] = {'type': 'object', 'properties': propiedades}

    especificacion_swagger = {
        'swagger': '2.0',
        'info': {
            'title': 'Documentación de la API generada automáticamente',
            'description': 'API REST generada automáticamente a partir de la base de datos',
            'version': '1.0.0'
        },
        'paths': paths,
        'definitions': modelos
    }
    return especificacion_swagger

# Genera el archivo donde se va a guardar el swagger **carpeta static**
def guardar_specs_swagger(app, db_session):
    especificacion_swagger = generar_swagger(app, db_session)
    carpeta_static = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(carpeta_static, exist_ok=True)
    with open(os.path.join(carpeta_static, 'swagger.json'), 'w') as f:
        json.dump(especificacion_swagger, f)
