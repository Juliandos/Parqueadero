from flask import Blueprint, jsonify, render_template, request
from app.models import VehiculoTipo, TarifaTipo, Tarifa, Modulo, Vehiculo, Parqueo, Punto, Redimir, Arrendamiento, Sede, Pais, Usuario, Rol, Periodicidad, Cliente, MedioPago, Parqueadero
from app import db
import bcrypt

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

# TarifaTipo ALL
@routes.route('/tarifa_tipo', methods=['GET'])
def tarifa_tipo():
    tarifas_tipo = TarifaTipo.query.all()
    return render_template('tarifa_tipo.html', titulo='Tipo de Tarifa', tipos_tarifa = tarifas_tipo)

# TarifaTipo CREATE
@routes.route('/tarifa_tipo/add', methods=['POST'])
def tarifa_tipo_add():
    data = request.get_json()
    nombre = data.get('nombre')
    unidad = data.get('unidad')
    if not nombre or not unidad:
        return jsonify({'success': False, 'message': 'Los campos nombre y unidad son obligatorios'}), 400
    
    nueva_tarifa = TarifaTipo(nombre=nombre, unidad=unidad)
    db.session.add(nueva_tarifa)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Tarifa agregada correctamente'})

# TarifaTipo UPDATE
@routes.route('/tarifa_tipo/edit/<int:id>', methods=['PUT'])
def tarifa_tipo_update(id):
    data = request.get_json()
    nombre = data.get('nombre')
    unidad = data.get('unidad')
    if not nombre or not unidad:
        return jsonify({'success': False, 'message': 'Los campos nombre y unidad son obligatorios'}), 400
    
    tarifa_tipo = TarifaTipo.query.get_or_404(id)
    tarifa_tipo.nombre = nombre
    tarifa_tipo.unidad = unidad
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Tarifa actualizada correctamente'}), 200

# TarifaTipo DELETE
@routes.route('/tarifa_tipo/delete/<int:id>', methods=['POST'])
def tarifa_tipo_delete(id):
    tarifa_tipo = TarifaTipo.query.get_or_404(id)
    
    if request.form.get('_method') == 'DELETE':  # Simular DELETE
        db.session.delete(tarifa_tipo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Tarifa eliminada'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# MedioPago ALL
@routes.route('/medio_pago', methods=['GET'])
def medio_pago():
    medios_pagos = MedioPago.query.all()
    return render_template('medio_pago.html', titulo='Medios de Pago', medios_pagos = medios_pagos)

# MedioPago CREATE
@routes.route('/medio_pago/add', methods=['POST'])
def add_medio_pago():
    data = request.get_json()
    nombre = data.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400
    
    nuevo_medio = MedioPago(nombre=nombre)
    db.session.add(nuevo_medio)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Medio de pago agregado correctamente'})

# MedioPago UPDATE
@routes.route('/medio_pago/edit/<int:id>', methods=['PUT'])
def update_medio_pago(id):
    data = request.get_json()
    nombre = data.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400
    
    medio_pago = MedioPago.query.get_or_404(id)
    medio_pago.nombre = nombre
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Medio de pago actualizado correctamente'}), 200

# MedioPago DELETE
@routes.route('/medio_pago/delete/<int:id>', methods=['POST'])
def delete_medio_pago(id):
    medio_pago = MedioPago.query.get_or_404(id)
    
    if request.form.get('_method') == 'DELETE':
        db.session.delete(medio_pago)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Medio de pago eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Cliente ALL
@routes.route('/cliente', methods=['GET'])
def cliente():
    clientes = Cliente.query.join(Parqueadero).add_columns(
        Cliente.id, Cliente.documento, Cliente.nombres, Cliente.apellidos, Cliente.telefono, Cliente.email, Cliente.direccion, Parqueadero.nombre.label('cliente_nombre')
    ).all()

    clientes_dict = [
        {
            "id": u.id,
            "documento": u.documento,
            "nombres": u.nombres,
            "apellidos": u.apellidos,
            "telefono": u.telefono,
            "email": u.email,
            "direccion": u.direccion,
            "cliente_nombre": u.cliente_nombre
        }
        for u in clientes
    ]
    return render_template('clientes.html', titulo='Clientes', clientes = clientes_dict)

# Rol ALL
@routes.route('/rol', methods=['GET'])
def rol():
    roles = Rol.query.all()
    return render_template('rol.html', titulo='Roles', roles = roles)

# Rol CREATE
@routes.route('/rol/add', methods=['POST'])
def add_rol():
    data = request.get_json()
    nombre = data.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400
    
    nuevo_rol = Rol(nombre=nombre)
    db.session.add(nuevo_rol)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Rol agregado correctamente'})

# Rol UPDATE
@routes.route('/rol/edit/<int:id>', methods=['PUT'])
def update_rol(id):
    data = request.get_json()
    nombre = data.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400
    
    rol = Rol.query.get_or_404(id)
    rol.nombre = nombre
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Rol actualizado correctamente'}), 200

# Rol DELETE
@routes.route('/rol/delete/<int:id>', methods=['POST'])
def delete_rol(id):
    rol = Rol.query.get_or_404(id)
    
    if request.form.get('_method') == 'DELETE':
        db.session.delete(rol)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Rol eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Usiario ALL
@routes.route('/usuario', methods=['GET'])
def usuario():
    usuarios = Usuario.query.join(Rol).add_columns(
        Usuario.id, Usuario.documento, Usuario.contrasena, Usuario.nombres, Usuario.apellidos, Usuario.telefono, Usuario.email, Usuario.direccion, Rol.nombre.label('rol_nombre')
    ).all()

    usuarios_dict = [
        {
            "id": u.id,
            "documento": u.documento,
            "contrasena": u.contrasena,
            "nombres": u.nombres,
            "apellidos": u.apellidos,
            "telefono": u.telefono,
            "email": u.email,
            "direccion": u.direccion,
            "rol_nombre": u.rol_nombre
        }
        for u in usuarios
    ]

    return render_template('usuario.html', titulo='Usuarios', usuarios=usuarios_dict)

# Usiario CREATE
@routes.route('/usuario/add', methods=['POST'])
def add_usuario():
    data = request.get_json()
    documento = data.get('documento')
    contrasena = data.get('contrasena')
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    direccion = data.get('direccion')
    rol_id = data.get('rol_id')

    if not documento or not contrasena or not nombres or not apellidos or not telefono or not email or not direccion or not rol_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    if Usuario.query.filter_by(documento=documento).first():   
        return jsonify({'success': False, 'message': 'El documento ya existe'}), 400
    
    nuevo_usuario = Usuario(documento=documento, contrasena=bcrypt.generate_password_hash(contrasena), nombres=nombres, apellidos=apellidos, telefono=telefono, email=email, direccion=direccion, rol_id=rol_id)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuario agregado correctamente'})
