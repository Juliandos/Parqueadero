from datetime import datetime
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

    clientes = Cliente.query.order_by(Cliente.id).all()
    vTipos = VehiculoTipo.query.order_by(VehiculoTipo.id).all()

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

# Vehículo CREATE
@routes.route('/vehiculo/add', methods=['POST'])
def add_vehiculo():
    data = request.get_json()
    placa = data.get('placa')
    marca = data.get('marca')
    modelo = data.get('modelo')
    vehiculo_tipo_id = data.get('vehiculo_tipo_id')
    cliente_id = data.get('cliente_id')
    
    if not placa or not marca or not modelo or not vehiculo_tipo_id or not cliente_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400
    
    if Vehiculo.query.filter_by(placa=placa).first():
        return jsonify({'success': False, 'message': 'La placa ya existe'}), 400
    
    nuevo_vehiculo = Vehiculo(placa=placa, marca=marca, modelo=modelo, vehiculo_tipo_id=vehiculo_tipo_id, cliente_id=cliente_id)
    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Vehículo agregado correctamente'})

# Vehiculo UPDATE
@routes.route('/vehiculo/edit/<int:id>', methods=['PUT'])
def update_vehiculo(id):
    data = request.get_json()
    placa = data.get('placa')
    marca = data.get('marca')
    modelo = data.get('modelo')
    vehiculo_tipo_id = data.get('vehiculo_tipo_id')
    cliente_id = data.get('cliente_id')
    
    if not placa or not marca or not modelo or not vehiculo_tipo_id or not cliente_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400
    
    vehiculo = Vehiculo.query.get_or_404(id)
    vehiculo.placa = placa
    vehiculo.marca = marca
    vehiculo.modelo = modelo
    vehiculo.vehiculo_tipo_id = vehiculo_tipo_id
    vehiculo.cliente_id = cliente_id
    db.session.commit()  # Se actualiza automáticamente `updated_at`
    
    return jsonify({'success': True, 'message': 'Vehículo actualizado correctamente'}), 200

# Vehículo DELETE
@routes.route('/vehiculo/delete/<string:id>', methods=['POST'])
def delete_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(vehiculo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Vehículo eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Tarifa ALL
@routes.route('/tarifa', methods=['GET'])
def tarifa():
    tarifas = Tarifa.query \
        .join(TarifaTipo) \
        .add_columns(
            Tarifa.id,
            Tarifa.nombre, 
            Tarifa.costo, 
            Tarifa.tarifacol,
            Tarifa.tarifa_tipo_id,
            TarifaTipo.nombre.label('tarifa_tipo_nombre')
        ) \
        .all()

    tarifa_tipos = TarifaTipo.query.order_by(TarifaTipo.id).all()

    tarifas_dict = [
        {
            "id": t.id,
            "nombre": t.nombre,
            "costo": t.costo,
            "tarifacol": t.tarifacol,
            "tarifa_tipo_id": t.tarifa_tipo_id,
            "tarifa_tipo_nombre": t.tarifa_tipo_nombre
        }
        for t in tarifas
    ]
    
    return render_template('tarifa.html', titulo='Tarifas', tarifas=tarifas_dict, tarifa_tipos=tarifa_tipos)

# Tarifa CREATE
@routes.route('/tarifa/add', methods=['POST'])
def add_tarifa():
    data = request.get_json()
    nombre = data.get('nombre')
    costo = data.get('costo')
    tarifacol = data.get('tarifacol')
    tarifa_tipo_id = data.get('tarifa_tipo_id')

    if not nombre or not costo or not tarifa_tipo_id:
        return jsonify({'success': False, 'message': 'Todos los campos obligatorios'}), 400

    nueva_tarifa = Tarifa(
        nombre=nombre, costo=costo, tarifacol=tarifacol, tarifa_tipo_id=tarifa_tipo_id
    )
    db.session.add(nueva_tarifa)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Tarifa agregada correctamente'})

# Tarifa UPDATE
@routes.route('/tarifa/edit/<int:id>', methods=['PUT'])
def update_tarifa(id):
    data = request.get_json()
    nombre = data.get('nombre')
    costo = data.get('costo')
    tarifacol = data.get('tarifacol')
    tarifa_tipo_id = data.get('tarifa_tipo_id')

    if not nombre or not costo or not tarifa_tipo_id:
        return jsonify({'success': False, 'message': 'Todos los campos obligatorios'}), 400

    tarifa = Tarifa.query.get_or_404(id)
    tarifa.nombre = nombre
    tarifa.costo = costo
    tarifa.tarifacol = tarifacol
    tarifa.tarifa_tipo_id = tarifa_tipo_id
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Tarifa actualizada correctamente'})

# Tarifa DELETE
@routes.route('/tarifa/delete/<int:id>', methods=['POST'])
def delete_tarifa(id):
    tarifa = Tarifa.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(tarifa)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Tarifa eliminada'}), 200

    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Parqueo ALL
@routes.route('/parqueo', methods=['GET'])
def listar_parqueos():
    parqueos = Parqueo.query \
        .join(Modulo) \
        .join(MedioPago) \
        .join(Tarifa) \
        .add_columns(
            Parqueo.id,
            Parqueo.fecha_entrada,
            Parqueo.fecha_salida,
            Parqueo.modulo_id,
            Parqueo.vehiculo_placa,
            Parqueo.medio_pago_id,
            Parqueo.tarifa_id,
            Modulo.nombre.label('modulo_nombre'),
            MedioPago.nombre.label('medio_pago_nombre'),
            Tarifa.nombre.label('tarifa_nombre')
        ) \
        .all()
    
    modulos = Modulo.query.order_by(Modulo.id).all()
    vehiculos = Vehiculo.query.order_by(Vehiculo.placa).all()
    medioPagos = MedioPago.query.order_by(MedioPago.id).all()
    tarifas = Tarifa.query.order_by(Tarifa.id).all()

    parqueos_dict = [
        {
            "id": p.id,
            "fecha_entrada": p.fecha_entrada,
            "fecha_salida": p.fecha_salida,
            "modulo": p.modulo_id,
            "vehiculo": p.vehiculo_placa,
            "medio_pago": p.medio_pago_id,
            "tarifa": p.tarifa_id,
            "modulo_nombre": p.modulo_nombre,
            "medio_pago_nombre": p.medio_pago_nombre,
            "tarifa_nombre": p.tarifa_nombre
        }
        for p in parqueos
    ]

    return render_template('parqueo.html', titulo='Parqueos', parqueos=parqueos_dict, modulos=modulos, vehiculos=vehiculos, medioPagos=medioPagos, tarifas=tarifas)

# Parqueo CREATE
@routes.route('/parqueo/add', methods=['POST'])
def agregar_parqueo():
    data = request.get_json()
    modulo_id = data.get('modulo_id')
    vehiculo_placa = data.get('vehiculo_placa')
    medio_pago_id = data.get('medio_pago_id')
    tarifa_id = data.get('tarifa_id')
    fecha_entrada = data.get('fecha_entrada')

    if not modulo_id or not vehiculo_placa or not medio_pago_id or not tarifa_id or not fecha_entrada:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    nuevo_parqueo = Parqueo(
        fecha_entrada=datetime.now(),
        modulo_id=modulo_id,
        vehiculo_placa=vehiculo_placa,
        medio_pago_id=medio_pago_id,
        tarifa_id=tarifa_id
    )

    db.session.add(nuevo_parqueo)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Parqueo registrado correctamente'})

# Parqueo UPDATE
@routes.route('/parqueo/edit/<int:id>', methods=['PUT'])
def actualizar_parqueo(id):
    data = request.get_json()
    print(data)
    modulo_id = data.get('modulo_id')
    vehiculo_placa = data.get('vehiculo_placa')
    medio_pago_id = data.get('medio_pago_id')
    tarifa_id = data.get('tarifa_id')
    fecha_salida = data.get('fecha_salida')

    parqueo = Parqueo.query.get_or_404(id)
    parqueo.fecha_salida = datetime.fromisoformat(fecha_salida)
    parqueo.modulo_id = modulo_id
    parqueo.vehiculo_placa = vehiculo_placa
    parqueo.medio_pago_id = medio_pago_id
    parqueo.tarifa_id = tarifa_id
    print(parqueo)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Parqueo actualizado correctamente'})

# Parqueo DELETE
@routes.route('/parqueo/delete/<int:id>', methods=['POST'])
def eliminar_parqueo(id):
    parqueo = Parqueo.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(parqueo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Parqueo eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Arrendamiento ALL
@routes.route('/arrendamiento', methods=['GET'])
def listar_arrendamientos():
    arrendamientos = Arrendamiento.query \
        .join(Periodicidad) \
        .join(Vehiculo) \
        .join(MedioPago) \
        .add_columns(
            Arrendamiento.id,
            Arrendamiento.descripcion,
            Arrendamiento.periodicidad_id,
            Arrendamiento.vehiculo_placa,
            Arrendamiento.medio_pago_id,
            Periodicidad.nombre.label('periodicidad_nombre'),
            Vehiculo.placa.label('vehiculo_placa'),
            MedioPago.nombre.label('medio_pago_nombre')
        ) \
        .all()
    
    periodicidades = Periodicidad.query.order_by(Periodicidad.id).all()
    vehiculos = Vehiculo.query.order_by(Vehiculo.placa).all()
    medioPagos = MedioPago.query.order_by(MedioPago.id).all()

    arrendamientos_dict = [
        {
            "id": a.id,
            "descripcion": a.descripcion,
            "periodicidad_id": a.periodicidad_id,
            "vehiculo_placa": a.vehiculo_placa,
            "medio_pago_id": a.medio_pago_id,
            "periodicidad_nombre": a.periodicidad_nombre,
            "vehiculo_placa": a.vehiculo_placa,
            "medio_pago_nombre": a.medio_pago_nombre
        }
        for a in arrendamientos
    ]

    return render_template('arrendamiento.html', 
                        titulo='Arrendamientos', 
                        arrendamientos=arrendamientos_dict,
                        periodicidades=periodicidades,
                        vehiculos=vehiculos,
                        medioPagos=medioPagos)

# Arrendamiento CREATE
@routes.route('/arrendamiento/add', methods=['POST'])
def agregar_arrendamiento():
    data = request.get_json()
    descripcion = data.get('descripcion')
    periodicidad_id = data.get('periodicidad_id')
    vehiculo_placa = data.get('vehiculo_placa')
    medio_pago_id = data.get('medio_pago_id')

    if not descripcion or not periodicidad_id or not vehiculo_placa or not medio_pago_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    nuevo_arrendamiento = Arrendamiento(
        descripcion=descripcion,
        periodicidad_id=periodicidad_id,
        vehiculo_placa=vehiculo_placa,
        medio_pago_id=medio_pago_id
    )

    db.session.add(nuevo_arrendamiento)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Arrendamiento creado correctamente'})

# Arrendamiento UPDATE
@routes.route('/arrendamiento/edit/<int:id>', methods=['PUT'])
def actualizar_arrendamiento(id):
    data = request.get_json()
    descripcion = data.get('descripcion')
    periodicidad_id = data.get('periodicidad_id')
    vehiculo_placa = data.get('vehiculo_placa')
    medio_pago_id = data.get('medio_pago_id')

    arrendamiento = Arrendamiento.query.get_or_404(id)
    arrendamiento.descripcion = descripcion
    arrendamiento.periodicidad_id = periodicidad_id
    arrendamiento.vehiculo_placa = vehiculo_placa
    arrendamiento.medio_pago_id = medio_pago_id
    arrendamiento.updated_at = datetime.now()

    db.session.commit()
    return jsonify({'success': True, 'message': 'Arrendamiento actualizado correctamente'})

# Arrendamiento DELETE
@routes.route('/arrendamiento/delete/<int:id>', methods=['POST'])
def eliminar_arrendamiento(id):
    arrendamiento = Arrendamiento.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(arrendamiento)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Arrendamiento eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Modulo ALL
@routes.route('/modulo', methods=['GET'])
def listar_modulos():
    modulos = Modulo.query \
        .join(Sede) \
        .add_columns(
            Modulo.id,
            Modulo.nombre,
            Modulo.habilitado,
            Modulo.descripcion,
            Modulo.sede_id,
            Sede.nombre.label('sede_nombre')
        ) \
        .all()
    
    sedes = Sede.query.order_by(Sede.id).all()

    modulos_dict = [
        {
            "id": m.id,
            "nombre": m.nombre,
            "habilitado": m.habilitado,
            "descripcion": m.descripcion,
            "sede_id": m.sede_id,
            "sede_nombre": m.sede_nombre
        }
        for m in modulos
    ]

    return render_template('modulo.html', 
                        titulo='Módulos', 
                        modulos=modulos_dict,
                        sedes=sedes)

# Modulo CREATE
@routes.route('/modulo/add', methods=['POST'])
def agregar_modulo():
    data = request.get_json()
    nombre = data.get('nombre')
    habilitado = data.get('habilitado')
    descripcion = data.get('descripcion')
    sede_id = data.get('sede_id')

    if not nombre or not sede_id or habilitado is None:
        return jsonify({'success': False, 'message': 'Nombre, Habilitado y Sede son obligatorios'}), 400

    nuevo_modulo = Modulo(
        nombre=nombre,
        habilitado=habilitado,
        descripcion=descripcion,
        sede_id=sede_id
    )

    db.session.add(nuevo_modulo)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Módulo creado correctamente'})

# Modulo UPDATE
@routes.route('/modulo/edit/<int:id>', methods=['PUT'])
def actualizar_modulo(id):
    data = request.get_json()
    modulo = Modulo.query.get_or_404(id)
    
    modulo.nombre = data.get('nombre', modulo.nombre)
    modulo.habilitado = data.get('habilitado', modulo.habilitado)
    modulo.descripcion = data.get('descripcion', modulo.descripcion)
    modulo.sede_id = data.get('sede_id', modulo.sede_id)
    modulo.updated_at = datetime.now()

    db.session.commit()
    return jsonify({'success': True, 'message': 'Módulo actualizado correctamente'})

# Modulo DELETE
@routes.route('/modulo/delete/<int:id>', methods=['POST'])
def eliminar_modulo(id):
    modulo = Modulo.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(modulo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Módulo eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Sede ALL
@routes.route('/sede', methods=['GET'])
def listar_sedes():
    sedes = Sede.query \
        .join(Parqueadero, Sede.parqueadero) \
        .join(Usuario, Sede.usuario) \
        .add_columns(
            Sede.id,
            Sede.nombre,
            Sede.direccion,
            Sede.telefono,
            Sede.email,
            Sede.ciudad,
            Sede.parqueadero_id,
            Sede.usuario_id,
            Parqueadero.nombre.label('parqueadero_nombre'),
            Usuario.nombres.label('usuario_nombre')
        ) \
        .all()
    
    parqueaderos = Parqueadero.query.order_by(Parqueadero.id).all()
    usuarios = Usuario.query.order_by(Usuario.id).all()

    sedes_dict = [
        {
            "id": s.id,
            "nombre": s.nombre,
            "direccion": s.direccion,
            "telefono": s.telefono,
            "email": s.email,
            "ciudad": s.ciudad,
            "parqueadero_id": s.parqueadero_id,
            "usuario_id": s.usuario_id,
            "parqueadero_nombre": s.parqueadero_nombre,
            "usuario_nombre": s.usuario_nombre
        }
        for s in sedes
    ]
    return render_template('sede.html', 
                        titulo='Sedes', 
                        sedes=sedes_dict,
                        parqueaderos=parqueaderos,
                        usuarios=usuarios)

# Sede CREATE
@routes.route('/sede/add', methods=['POST'])
def agregar_sede():
    data = request.get_json()
    required_fields = ['nombre', 'direccion', 'telefono', 'email', 'ciudad', 'parqueadero_id', 'usuario_id']
    
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    nueva_sede = Sede(
        nombre=data['nombre'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        email=data['email'],
        ciudad=data['ciudad'],
        parqueadero_id=data['parqueadero_id'],
        usuario_id=data['usuario_id']
    )

    db.session.add(nueva_sede)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Sede creada correctamente'})

# Sede UPDATE
@routes.route('/sede/edit/<int:id>', methods=['PUT'])
def actualizar_sede(id):
    data = request.get_json()
    sede = Sede.query.get_or_404(id)
    
    sede.nombre = data.get('nombre', sede.nombre)
    sede.direccion = data.get('direccion', sede.direccion)
    sede.telefono = data.get('telefono', sede.telefono)
    sede.email = data.get('email', sede.email)
    sede.ciudad = data.get('ciudad', sede.ciudad)
    sede.parqueadero_id = data.get('parqueadero_id', sede.parqueadero_id)
    sede.usuario_id = data.get('usuario_id', sede.usuario_id)
    sede.updated_at = datetime.now()

    db.session.commit()
    return jsonify({'success': True, 'message': 'Sede actualizada correctamente'})

# Sede DELETE
@routes.route('/sede/delete/<int:id>', methods=['POST'])
def eliminar_sede(id):
    sede = Sede.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(sede)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Sede eliminada'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Pais LIST
@routes.route('/pais', methods=['GET'])
def listar_paises():
    paises = Pais.query.all()
    
    paises_dict = [
        {
            "id": p.id,
            "nombre": p.nombre
        }
        for p in paises
    ]
    return render_template('pais.html', 
                        titulo='Países', 
                        paises=paises_dict)

# Pais CREATE
@routes.route('/pais/add', methods=['POST'])
def agregar_pais():
    data = request.get_json()
    
    if not data.get('nombre'):
        return jsonify({'success': False, 'message': 'El nombre es obligatorio'}), 400

    nuevo_pais = Pais(
        nombre=data['nombre']
    )

    db.session.add(nuevo_pais)
    db.session.commit()
    return jsonify({'success': True, 'message': 'País creado correctamente'})

# Pais UPDATE
@routes.route('/pais/edit/<int:id>', methods=['PUT'])
def actualizar_pais(id):
    data = request.get_json()
    pais = Pais.query.get_or_404(id)
    
    pais.nombre = data.get('nombre', pais.nombre)
    pais.updated_at = datetime.now()

    db.session.commit()
    return jsonify({'success': True, 'message': 'País actualizado correctamente'})

# Pais DELETE
@routes.route('/pais/delete/<int:id>', methods=['POST'])
def eliminar_pais(id):
    pais = Pais.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(pais)
        db.session.commit()
        return jsonify({'success': True, 'message': 'País eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Periodicidad ALL
@routes.route('/periodicidad', methods=['GET'])
def listar_periodicidades():
    periodicidades = Periodicidad.query.all()
    
    periodicidades_dict = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "dias": p.dias
        }
        for p in periodicidades
    ]
    return render_template('periodicidad.html', 
                        titulo='Periodicidades', 
                        periodicidades=periodicidades_dict)

# Periodicidad CREATE
@routes.route('/periodicidad/add', methods=['POST'])
def agregar_periodicidad():
    data = request.get_json()
    
    if not data.get('nombre') or not data.get('dias'):
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    nueva_periodicidad = Periodicidad(
        nombre=data['nombre'],
        dias=data['dias']
    )

    db.session.add(nueva_periodicidad)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Periodicidad creada correctamente'})

# Periodicidad UPDATE
@routes.route('/periodicidad/edit/<int:id>', methods=['PUT'])
def actualizar_periodicidad(id):
    data = request.get_json()
    periodicidad = Periodicidad.query.get_or_404(id)
    
    periodicidad.nombre = data.get('nombre', periodicidad.nombre)
    periodicidad.dias = data.get('dias', periodicidad.dias)
    periodicidad.updated_at = datetime.now()

    db.session.commit()
    return jsonify({'success': True, 'message': 'Periodicidad actualizada correctamente'})

# Periodicidad DELETE
@routes.route('/periodicidad/delete/<int:id>', methods=['POST'])
def eliminar_periodicidad(id):
    periodicidad = Periodicidad.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(periodicidad)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Periodicidad eliminada'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Puntos ALL
@routes.route('/puntos')
def obtener_puntos():
    puntos = Punto.query.join(Cliente).add_columns(
        Punto.id,
        Punto.cantidad,
        Cliente.nombres.label('cliente_nombre'),
    ).all()

    clientes = Cliente.query.order_by(Cliente.id).all()

    puntos_data = [{
        'id': p.id,
        'cantidad': p.cantidad,
        'cliente': p.cliente_nombre
    } for p in puntos]

    return render_template('puntos.html', 
                        titulo="Administración de Puntos",
                        puntos=puntos_data,
                        clientes=clientes)

# Puntos CREATE
@routes.route('/punto/add', methods=['POST'])
def agregar_punto():
    data = request.get_json()
    cantidad = data.get('cantidad')
    cliente_id = data.get('cliente_id')
    
    if not cantidad or not cliente_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    nuevo_punto = Punto(
        cantidad=cantidad,
        cliente_id=cliente_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.session.add(nuevo_punto)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Punto creado correctamente'})

# Puntos UPDATE
@routes.route('/punto/edit/<int:id>', methods=['PUT'])
def actualizar_punto(id):
    data = request.get_json()
    punto = Punto.query.get_or_404(id)
    
    punto.cantidad = data.get('cantidad', punto.cantidad)
    punto.cliente_id = data.get('cliente_id', punto.cliente_id)
    punto.updated_at = datetime.now()
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Punto actualizado correctamente'})

# Puntos DELETE
@routes.route('/punto/delete/<int:id>', methods=['POST'])
def eliminar_punto(id):
    punto = Punto.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(punto)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Punto eliminado'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Redimir ALL
@routes.route('/redimir')
def obtener_redenciones():
    redenciones = Redimir.query.join(Punto).add_columns(
        Redimir.id,
        Redimir.cantidad,
        Punto.id.label('punto_id'),
        Punto.cantidad.label('punto_cantidad')
    ).all()

    puntos = Punto.query.order_by(Punto.id).all()

    redenciones_data = [{
        'id': r.id,
        'cantidad': r.cantidad,
        'punto_id': r.punto_id,
        'punto_cantidad': r.punto_cantidad  
    } for r in redenciones]

    return render_template('redimir.html', 
                        titulo="Administración de Redenciones",
                        redenciones=redenciones_data,
                        puntos=puntos)

# Redimir CREATE
@routes.route('/redimir/add', methods=['POST'])
def agregar_redencion():
    data = request.get_json()
    cantidad = data.get('cantidad')
    puntos_id = data.get('puntos_id')
    
    if not cantidad or not puntos_id:
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    nuevo_redimir = Redimir(
        cantidad=cantidad,
        punto_id=puntos_id
    )

    db.session.add(nuevo_redimir)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Redención registrada correctamente'})

# Redimir UPDATE
@routes.route('/redimir/edit/<int:id>', methods=['PUT'])
def actualizar_redencion(id):
    data = request.get_json()
    redimir = Redimir.query.get_or_404(id)
    
    redimir.cantidad = data.get('cantidad', redimir.cantidad)
    redimir.punto_id = data.get('puntos_id', redimir.punto_id)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Redención actualizada correctamente'})

# Redimir DELETE
@routes.route('/redimir/delete/<int:id>', methods=['POST'])
def eliminar_redencion(id):
    redimir = Redimir.query.get_or_404(id)

    if request.form.get('_method') == 'DELETE':
        db.session.delete(redimir)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Redención eliminada'}), 200
    
    return jsonify({'success': False, 'message': 'Método no permitido'}), 400

# Parqueadero ALL
@routes.route('/parqueadero', methods=['GET'])
def listar_parqueaderos():
    parqueaderos = Parqueadero.query \
        .join(Usuario) \
        .join(Pais) \
        .add_columns(
            Parqueadero.id,
            Parqueadero.rut,
            Parqueadero.nombre,
            Parqueadero.direccion,
            Parqueadero.telefono,
            Parqueadero.email,
            Parqueadero.ciudad,
            Parqueadero.pais_id,
            Parqueadero.usuario_id,
            Parqueadero.created_at,
            Parqueadero.updated_at,
            Usuario.nombres.label('usuario_nombre'),
            Pais.nombre.label('pais_nombre')
        ) \
        .all()
    
    usuarios = Usuario.query.order_by(Usuario.nombres).all()
    paises = Pais.query.order_by(Pais.nombre).all()

    parqueaderos_dict = [
        {
            "id": p.id,
            "rut": p.rut,
            "nombre": p.nombre,
            "direccion": p.direccion,
            "telefono": p.telefono,
            "email": p.email,
            "ciudad": p.ciudad,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "usuario_id": p.usuario_id,
            "pais_id": p.pais_id,
            "usuario_nombre": p.usuario_nombre,
            "pais_nombre": p.pais_nombre
        }
        for p in parqueaderos
    ]

    return render_template('parqueadero.html', 
                        titulo='Parqueaderos',
                        parqueaderos=parqueaderos_dict,
                        usuarios=usuarios,
                        paises=paises)

# Parqueadero CREATE
@routes.route('/parqueadero/add', methods=['POST'])
def agregar_parqueadero():
    data = request.get_json()
    
    required_fields = ['rut', 'nombre', 'direccion', 'telefono', 'email', 'ciudad', 'usuario_id', 'pais_id']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

    if Parqueadero.query.filter_by(rut=data['rut']).first():
        return jsonify({'success': False, 'message': 'RUT ya registrado'}), 400

    nuevo_parqueadero = Parqueadero(
        rut=data['rut'],
        nombre=data['nombre'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        email=data['email'],
        ciudad=data['ciudad'],
        usuario_id=data['usuario_id'],
        pais_id=data['pais_id']
    )

    db.session.add(nuevo_parqueadero)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Parqueadero registrado correctamente'})

# Parqueadero UPDATE
@routes.route('/parqueadero/edit/<int:id>', methods=['PUT'])
def actualizar_parqueadero(id):
    data = request.get_json()
    parqueadero = Parqueadero.query.get_or_404(id)
    
    if Parqueadero.query.filter(Parqueadero.rut == data['rut'], Parqueadero.id != id).first():
        return jsonify({'success': False, 'message': 'RUT ya está en uso'}), 400

    parqueadero.rut = data['rut']
    parqueadero.nombre = data['nombre']
    parqueadero.direccion = data['direccion']
    parqueadero.telefono = data['telefono']
    parqueadero.email = data['email']
    parqueadero.ciudad = data['ciudad']
    parqueadero.usuario_id = data['usuario_id']
    parqueadero.pais_id = data['pais_id']

    db.session.commit()
    return jsonify({'success': True, 'message': 'Parqueadero actualizado correctamente'})

# Parqueadero DELETE
@routes.route('/parqueadero/delete/<int:id>', methods=['DELETE'])
def eliminar_parqueadero(id):
    parqueadero = Parqueadero.query.get_or_404(id)
    db.session.delete(parqueadero)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Parqueadero eliminado'}), 200