import os
from pathlib import Path
from dotenv import load_dotenv 

class Config:
    # Configuración base de la base de datos
    BASE_DIR = Path(__file__).resolve().parent.parent
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE') or \
        f'sqlite:///{BASE_DIR / "app.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False