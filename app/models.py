import os
from app import db
from datetime import datetime


def current_time():
    return datetime.utcnow()

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


# Continuar con los modelos restantes de forma similar
