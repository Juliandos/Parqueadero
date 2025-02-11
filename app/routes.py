from flask import Blueprint, jsonify, render_template, request
from app.models import VehiculoTipo, TarifaTipo, Tarifa, Modulo, Vehiculo, Parqueo, Punto, Redimir, Arrendamiento, Sede, Pais, Usuario, Rol, Periodicidad, Cliente, MedioPago, Parqueadero
from app import db

routes = Blueprint('routes', __name__)

info_template = {
    'titulo': 'Inicio',
    'nombre': 'Julian'
}

@routes.route('/')
def index():
    return render_template('index.html', info_template=info_template)

# VehiculoTipo all
@routes.route('/vehiculo_tipo')
def vehiculo_tipo():
    tipos_vehiculo = VehiculoTipo.query.all()
    return render_template('vehiculo_tipo.html', titulo='Tipo de Vehiculo', tipos_vehiculo = tipos_vehiculo)

# VehiculoTipo DELETE
@routes.route('/vehiculo_tipo/delete/<int:id>', methods=['POST'])
def vehiculo_tipo_delete(id):
    tipo_vehiculo = VehiculoTipo.query.get_or_404(id)
    
    if request.form.get('_method') == 'DELETE':  # Simular DELETE
        db.session.delete(tipo_vehiculo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Vehículo eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# VehiculoTipo CREATE
@routes.route('/vehiculo_tipo/add', methods=['POST'])
def vehiculo_tipo_add():
    data = request.get_json()
    nombre = data.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400
    
    nuevo_tipo = VehiculoTipo(nombre=nombre)
    db.session.add(nuevo_tipo)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Vehículo agregado correctamente'})

# VehiculoTipo EDIT
@routes.route('/vehiculo_tipo/edit/<int:id>', methods=['PUT'])
def vehiculo_tipo_edit(id):
    data = request.get_json()
    nombre = data.get('nombre')

    tipo_vehiculo = VehiculoTipo.query.get_or_404(id)
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400

    tipo_vehiculo.nombre = nombre
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Vehículo actualizado correctamente'}), 200