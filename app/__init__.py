import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crear la app Flask
app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

# Configuración de la base de datos (ejemplo: SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva mensajes de advertencia


from app import routes