import os
from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crear la app Flask
app = Flask(__name__)

current_path = os.getcwd()
ruta_db = f'{current_path}/app.db'

# Configuración de la base de datos (ejemplo: SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{ruta_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva mensajes de advertencia

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definir un modelo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

with app.app_context():
    db.create_all()  # Crear la base de datos si no existe

    new_user = User(username='Julian', email='julian@gmail.com')
    db.session.add(new_user)
    db.session.commit()
    print(f"Usuario creado: {new_user}")
    users = User.query.all()
    print("Todos los usuarios:")
    print(users)

@app.route('/')
def home():
    return "Welcome to Flask-SQLAlchemy Example!"

if __name__ == '__main__':
    app.run(debug=True)
