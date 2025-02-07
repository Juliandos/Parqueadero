from flask import Blueprint, render_template
# from app import app
routes = Blueprint('routes', __name__)

info_template = {
    'titulo': 'Inicio',
    'nombre': 'Julian'
}

@routes.route('/')
def index():
    return render_template('index.html', info_template=info_template)

@routes.route('/vehiculo_tipo')
def vehiculo_tipo():
    return render_template('vehiculo_tipo.html', titulo='Tipo de Vehiculo')