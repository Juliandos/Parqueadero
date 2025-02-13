from flask import Blueprint, jsonify, render_template, request
from app.models import VehiculoTipo, TarifaTipo, Tarifa, Modulo, Vehiculo, Parqueo, Punto, Redimir, Arrendamiento, Sede, Pais, Usuario, Rol, Periodicidad, Cliente, MedioPago, Parqueadero
from app import db
import bcrypt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

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

    # Verificar si el usuario está asociado a parqueadero
    if VehiculoTipo.query.filter_by(vehiculo_tipo_id=id).first():
        return jsonify({'success': False, 'message': 'No se puede eliminar: usuario en uso'})
    
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
        return jsonify({'error': False, 'message': 'El nombre es obligatorio o es igual a otro'}), 400
    
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
        Cliente.id, Cliente.documento, Cliente.nombres, Cliente.apellidos, Cliente.telefono, Cliente.email, Cliente.direccion, Parqueadero.id.label('parqueadero_id'), Parqueadero.nombre.label('parqueadero_nombre')
    ).all()

    parqueaderos = Parqueadero.query.order_by(Parqueadero.id).all()  # Obtener TODOS los parqueaderos ordenados por ID

    clientes_dict = [
        {
            "id": u.id,
            "documento": u.documento,
            "nombres": u.nombres,
            "apellidos": u.apellidos,
            "telefono": u.telefono,
            "email": u.email,
            "direccion": u.direccion,
            "parqueadero_nombre": u.parqueadero_nombre
        }
        for u in clientes
    ]
    return render_template('clientes.html', titulo='Clientes', clientes = clientes_dict, parqueaderos=parqueaderos)

# Cliente CREATE
@routes.route('/cliente/add', methods=['POST'])
def add_cliente():
    data = request.get_json()
    documento = data.get('documento')
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    direccion = data.get('direccion')
    parqueadero_id = data.get('parqueadero_id')

    if not documento or not nombres or not apellidos or not telefono or not email or not direccion or not parqueadero_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400
    
    nuevo_cliente = Cliente(documento=documento, nombres=nombres, apellidos=apellidos, telefono=telefono, email=email, direccion=direccion, parqueadero_id=parqueadero_id)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Cliente agregado correctamente'})

# Cliente UPDATE
@routes.route('/cliente/edit/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    documento = data.get('documento')
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    direccion = data.get('direccion')
    parqueadero_id = data.get('parqueadero_id')
    
    if not documento or not nombres or not apellidos or not telefono or not email or not direccion or not parqueadero_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400
    
    cliente = Cliente.query.get_or_404(id)
    cliente.documento = documento
    cliente.nombres = nombres
    cliente.apellidos = apellidos
    cliente.telefono = telefono
    cliente.email = email
    cliente.direccion = direccion
    cliente.parqueadero_id = parqueadero_id
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Cliente actualizado correctamente'}), 200

# Cliente DELETE
@routes.route('/cliente/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.form.get('_method') == 'DELETE':
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cliente eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

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
        Usuario.id, Usuario.documento, Usuario.contrasena, Usuario.nombres, Usuario.apellidos, Usuario.telefono, Usuario.email, Usuario.ciudad, Usuario.direccion, Usuario.rol_id, Rol.nombre.label('rol_nombre')
    ).all()

    roles = Rol.query.order_by(Rol.id).all()  # Obtener TODOS los parqueaderos ordenados por ID

    usuarios_dict = [
        {
            "id": u.id,
            "documento": u.documento,
            "contrasena": u.contrasena,
            "nombres": u.nombres,
            "apellidos": u.apellidos,
            "telefono": u.telefono,
            "email": u.email,
            "ciudad": u.ciudad,
            "direccion": u.direccion,
            "direccion": u.direccion,
            "rol_id": u.rol_id,
            "rol_nombre": u.rol_nombre
        }
        for u in usuarios
    ]

    return render_template('usuario.html', titulo='Usuarios', usuarios=usuarios_dict, roles=roles)

# Usiario CREATE
@routes.route('/usuario/add', methods=['POST'])
def add_usuario():
    data = request.get_json()
    print(data)
    documento = data.get('documento')
    contrasena = bcrypt.generate_password_hash(data.get('contrasena')).decode('utf-8')
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    ciudad = data.get('ciudad')
    direccion = data.get('direccion')
    rol_id = data.get('rol_id')

    print("contrasena", contrasena)

    if not documento or not contrasena or not nombres or not apellidos or not telefono or not email or not ciudad or not direccion or not rol_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    if Usuario.query.filter_by(documento=documento).first():   
        return jsonify({'success': False, 'message': 'El documento ya existe'}), 400
    
    nuevo_usuario = Usuario(documento=documento, contrasena=contrasena, nombres=nombres, apellidos=apellidos, telefono=telefono, email=email, ciudad=ciudad, direccion=direccion, rol_id=rol_id)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuario agregado correctamente'})

# Usiario UPDATE
@routes.route('/usuario/edit/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    documento = data.get('documento')
    contrasena = data.get('contrasena')
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    ciudad = data.get('ciudad')
    direccion = data.get('direccion')
    rol_id = data.get('rol_id')
    
    if not documento or not nombres or not apellidos or not telefono or not email or not ciudad or not direccion or not rol_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400
    
    if contrasena:
        contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    
    usuario = Usuario.query.get_or_404(id)
    usuario.documento = documento
    usuario.contrasena = contrasena
    usuario.nombres = nombres
    usuario.apellidos = apellidos
    usuario.telefono = telefono
    usuario.email = email
    usuario.ciudad = ciudad
    usuario.direccion = direccion
    usuario.rol_id = rol_id
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Usuario actualizado correctamente'}), 200

# Usiario DELETE
@routes.route('/usuario/delete/<int:id>', methods=['POST'])
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    # Verificar si el usuario está asociado a parqueadero
    if Parqueadero.query.filter_by(usuario_id=id).first():
        return jsonify({'success': False, 'message': 'No se puede eliminar: usuario en uso'})
    
    if request.form.get('_method') == 'DELETE':
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Usuario eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Vehículo ALL
@routes.route('/vehiculo', methods=['GET'])
def vehiculo():
    vehiculos = Vehiculo.query \
        .join(VehiculoTipo) \
        .join(Cliente, Vehiculo.cliente_id == Cliente.id) \
        .add_columns(
            Vehiculo.placa, 
            Vehiculo.marca, 
            Vehiculo.modelo, 
            Vehiculo.vehiculo_tipo_id, 
            Vehiculo.cliente_id, 
            VehiculoTipo.nombre.label('vehiculo_tipo_nombre'),
            Cliente.nombres.label('cliente_nombre')
        ) \
        .all()

    vTipos = VehiculoTipo.query.order_by(VehiculoTipo.id).all()
    clientes = Cliente.query.order_by(Cliente.id).all()

    vehiculos_dict = [
        {
            "placa": v.placa,
            "marca": v.marca,
            "modelo": v.modelo,
            "vehiculo_tipo_id": v.vehiculo_tipo_id,
            "cliente_id": v.cliente_id,
            "vehiculo_tipo_nombre": v.vehiculo_tipo_nombre,
            "cliente_nombre": v.cliente_nombre
        }
        for v in vehiculos
    ]
    
    return render_template('vehiculo.html', titulo='Vehículos', vehiculos=vehiculos_dict, clientes=clientes, vTipos=vTipos)
