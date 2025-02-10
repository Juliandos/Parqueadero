from datetime import datetime
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar configuración desde la clase
    app.config.from_object(Config) 

    db.init_app(app)

    from app import models  # Importar modelos

    with app.app_context():
        db.create_all()
        seed_initial_data()

    from app.routes import routes  
    app.register_blueprint(routes)

    return app

def seed_initial_data():
    from app.models import VehiculoTipo  # Importar dentro del contexto
    
    if VehiculoTipo.query.count() == 0: # VehiculoTipo.query.first( )

        tipos = [
            VehiculoTipo(
                nombre='Adlai',
                created_at=datetime.strptime('12/11/2024', '%m/%d/%Y'),
                updated_at=datetime.strptime('12/20/2024', '%m/%d/%Y')
            ),
            VehiculoTipo(
                nombre='Phylys',
                created_at=datetime.strptime('03/23/2024', '%m/%d/%Y'),
                updated_at=datetime.strptime('06/29/2024', '%m/%d/%Y')
            ),
            VehiculoTipo(
                nombre='Suki',
                created_at=datetime.strptime('05/30/2024', '%m/%d/%Y'),
                updated_at=datetime.strptime('03/12/2024', '%m/%d/%Y')
            ),
            VehiculoTipo(
                nombre='Dari',
                created_at=datetime.strptime('10/19/2024', '%m/%d/%Y'),
                updated_at=datetime.strptime('11/28/2024', '%m/%d/%Y')
            ),
            VehiculoTipo(
                nombre='Cassie',
                created_at=datetime.strptime('03/30/2024', '%m/%d/%Y'),
                updated_at=datetime.strptime('03/13/2024', '%m/%d/%Y')
            )
        ]
        
        db.session.bulk_save_objects(tipos)
        db.session.commit()
        print("✅ Datos iniciales de vehiculo_tipo cargados")