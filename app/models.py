from . import db
from datetime import datetime


def current_time():
    return datetime.utcnow()

class TarifaTipo(db.Model):
    __tablename__ = 'tarifa_tipo'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(64), nullable=False)
    unidad = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<TarifaTipo {self.nombre}, Unidad: {self.unidad}>'

class Tarifa(db.Model):
    __tablename__ = 'tarifa'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    costo = db.Column(db.Float(precision=2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    tarifacol = db.Column(db.String(45), nullable=True)
    tarifa_tipo_id = db.Column(db.Integer, db.ForeignKey('tarifa_tipo.id'), nullable=False)
    
    tarifa_tipo = db.relationship('TarifaTipo', backref=db.backref('tarifas', lazy=True))

    def __repr__(self):
        return f'<Tarifa {self.nombre}, Costo: {self.costo}>'

class Parqueo(db.Model):
    __tablename__ = 'parqueo'  # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria
    fecha_entrada = db.Column(db.DateTime, default=current_time, nullable=False)  # Fecha de entrada
    fecha_salida = db.Column(db.DateTime, nullable=True)  # Fecha de salida (puede ser nulo)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)  # Fecha de creación
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)  # Fecha de actualización

    # Claves foráneas
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)  # Relación con 'modulo'
    vehiculo_placa = db.Column(db.Integer, db.ForeignKey('vehiculo.placa'), nullable=False)  # Relación con 'vehiculo'
    medio_pago_id = db.Column(db.Integer, db.ForeignKey('medio_pago.id'), nullable=False)  # Relación con 'medio_pago'
    tarifa_id = db.Column(db.Integer, db.ForeignKey('tarifa.id'), nullable=False)  # Relación con 'tarifa'

    # Relaciones con otras tablas
    modulo = db.relationship('Modulo', back_populates='parqueos')  # Relación con 'modulo'
    vehiculo = db.relationship('Vehiculo', back_populates='parqueos')  # Relación con 'vehiculo'
    medio_pago = db.relationship('MedioPago', back_populates='parqueos')  # Relación con 'medio_pago'
    tarifa = db.relationship('Tarifa', back_populates='parqueos')  # Relación con 'tarifa'

class Puntos(db.Model):
    __tablename__ = 'puntos'  # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria
    cantidad = db.Column(db.Integer, nullable=True)  # Cantidad de puntos (puede ser nulo)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)  # Fecha de creación
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)  # Fecha de actualización
    puntoscol = db.Column(db.String(45), nullable=True)  # Columna adicional (opcional)

    # Clave foránea
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)  # Relación con 'cliente'

    # Relación con la tabla 'cliente'
    cliente = db.relationship('Cliente', back_populates='puntos')

    # Relación inversa con la tabla 'redimir'
    redenciones = db.relationship('Redimir', back_populates='puntos')

class Redimir(db.Model):
    __tablename__ = 'redimir'  # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria
    cantidad = db.Column(db.Integer, nullable=False)  # Cantidad de puntos redimidos
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)  # Fecha de creación
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)  # Fecha de actualización
    redimircol = db.Column(db.String(45), nullable=True)  # Columna adicional (opcional)

    # Clave foránea
    puntos_id = db.Column(db.Integer, db.ForeignKey('puntos.id'), nullable=False)  # Relación con 'puntos'

    # Relación con la tabla 'puntos'
    puntos = db.relationship('Puntos', back_populates='redenciones')

class Arrendamiento(db.Model):
    __tablename__ = 'arrendamiento'  # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Clave primaria
    descripcion = db.Column(db.String(256), nullable=False)  # Descripción del arrendamiento
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)  # Fecha de creación
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)  # Fecha de actualización

    # Claves foráneas
    periodicidad_id = db.Column(db.Integer, db.ForeignKey('periodicidad.id'), nullable=False)  # Relación con 'periodicidad'
    vehiculo_placa = db.Column(db.Integer, db.ForeignKey('vehiculo.placa'), nullable=False)  # Relación con 'vehiculo'
    medio_pago_id = db.Column(db.Integer, db.ForeignKey('medio_pago.id'), nullable=False)  # Relación con 'medio_pago'

    # Relaciones con otras tablas
    periodicidad = db.relationship('Periodicidad', back_populates='arrendamientos')  # Relación con 'periodicidad'
    vehiculo = db.relationship('Vehiculo', back_populates='arrendamientos')  # Relación con 'vehiculo'
    medio_pago = db.relationship('MedioPago', back_populates='arrendamientos')  # Relación con 'medio_pago'

class Sede(db.Model):
    __tablename__ = 'sede'  

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    ciudad = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)

    modulos = db.relationship('Modulo', back_populates='sede')

class Pais(db.Model):
    __tablename__ = 'pais'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)

    parqueaderos = db.relationship('Parqueadero', back_populates='pais')

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(16), nullable=False)
    nombres = db.Column(db.String(32), nullable=False)
    apellidos = db.Column(db.String(32), nullable=False)
    telefono = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

    parqueaderos = db.relationship('Parqueadero', back_populates='usuario')

class Rol(db.Model):
    __tablename__ = 'rol'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)

class Periodicidad(db.Model):
    __tablename__ = 'periodicidad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    dias = db.Column(db.Integer, nullable=False)

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(16), nullable=False, unique=True)
    nombres = db.Column(db.String(32), nullable=False)
    apellidos = db.Column(db.String(32), nullable=False)
    telefono = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    parqueadero_id = db.Column(db.Integer, db.ForeignKey('parqueadero.id'), nullable=False)

class MedioPago(db.Model):
    __tablename__ = 'medio_pago'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'

    placa = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(12))
    modelo = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    vehiculo_tipo_id = db.Column(db.Integer, db.ForeignKey('vehiculo_tipo.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

class VehiculoTipo(db.Model):
    __tablename__ = 'vehiculo_tipo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)

class Modulo(db.Model):
    __tablename__ = 'modulo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), nullable=False)
    habilitado = db.Column(db.Boolean, default=True, nullable=False)
    descripcion = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    sede_id = db.Column(db.Integer, db.ForeignKey('sede.id'), nullable=False)

class Parqueadero(db.Model):
    __tablename__ = 'parqueadero'

    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(32), nullable=False, unique=True)
    nombre = db.Column(db.String(64), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    ciudad = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='parqueaderos')
    pais = db.relationship('Pais', back_populates='parqueaderos')

