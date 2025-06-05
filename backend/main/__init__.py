from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path
import os

# Inicializamos restful
api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Carga variables del .env

    # Obtener rutas desde variables de entorno
    db_dir = Path(os.getenv('DATABASE_PATH'))
    db_name = os.getenv('DATABASE_NAME')
    db_path = db_dir / db_name

    # Asegurarse de que el directorio exista
    db_dir.mkdir(parents=True, exist_ok=True)

    # Crear el archivo si no existe (multiplataforma)
    if not db_path.exists():
        db_path.touch()

    # Configuración de SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path.resolve())
    db.init_app(app)

    # Cargar los recursos
    import main.resources as resources
    api.add_resource(resources.NotificacionesResource, "/notificaciones")

    api.add_resource(resources.PedidosResource, "/pedidos")
    api.add_resource(resources.PedidoResource, "/pedido/<int:id>")

    api.add_resource(resources.ProductosResource, "/productos")
    api.add_resource(resources.ProductoResource, "/producto/<int:id>")

    api.add_resource(resources.UsuariosResource, "/usuarios")
    api.add_resource(resources.UsuarioResource, "/usuario/<int:id>")

    api.add_resource(resources.ValoracionesResource, "/valoraciones")

    api.add_resource(resources.LoginResource, "/login/")
    api.add_resource(resources.LogoutResource, "/logout/")

    # Inicializar la API
    api.init_app(app)

    return app
