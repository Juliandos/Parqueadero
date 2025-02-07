from flask import render_template
from app import app

info_template = {
    'titulo': 'Inicio',
    'nombre': 'Julian'
}

@app.route('/')
def index():
    return render_template('index.html', info_template=info_template)

@app.route('/vehiculo_tipo')
def vehiculo_tipo():
    return render_template('vehiculo_tipo.html', titulo='Tipo de Vehiculo')