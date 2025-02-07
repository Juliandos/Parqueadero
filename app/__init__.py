import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

    db.init_app(app)

    from app import models  # Importar modelos

    with app.app_context():
        db.create_all()

    # Importar y registrar el Blueprint de rutas
    from app.routes import routes  
    app.register_blueprint(routes)  # Registrar Blueprint correctamente

    return app
