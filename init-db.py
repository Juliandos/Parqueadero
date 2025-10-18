#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de prueba.
Ejecutar después del primer despliegue para poblar la base de datos.
"""

import os
import sys
from datetime import datetime

# Agregar el directorio actual al path para importar la aplicación
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    VehiculoTipo, TarifaTipo, Tarifa, Modulo, Vehiculo, Parqueo, 
    Punto, Redimir, Arrendamiento, Sede, Pais, Usuario, Rol, 
    Periodicidad, Cliente, MedioPago, Parqueadero
)

def init_database():
    """Inicializa la base de datos con datos de prueba."""
    
    print("🚀 Iniciando inicialización de la base de datos...")
    
    # Crear la aplicación
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        print("📋 Creando tablas de la base de datos...")
        db.create_all()
        
        # Verificar si ya hay datos
        if Usuario.query.count() > 0:
            print("⚠️  La base de datos ya contiene datos. ¿Deseas continuar? (y/N)")
            response = input().strip().lower()
            if response != 'y':
                print("❌ Inicialización cancelada.")
                return
        
        print("🌱 Insertando datos iniciales...")
        
        # Insertar países
        if Pais.query.count() == 0:
            paises = [
                Pais(id=1, nombre='Colombia', created_at=datetime(2024, 1, 27), updated_at=datetime(2025, 1, 4)),
                Pais(id=2, nombre='México', created_at=datetime(2024, 5, 28), updated_at=datetime(2024, 7, 6)),
                Pais(id=3, nombre='Argentina', created_at=datetime(2024, 2, 13), updated_at=datetime(2024, 2, 6)),
                Pais(id=4, nombre='Chile', created_at=datetime(2024, 6, 12), updated_at=datetime(2024, 12, 28)),
                Pais(id=5, nombre='Perú', created_at=datetime(2025, 1, 1), updated_at=datetime(2024, 6, 5)),
            ]
            db.session.bulk_save_objects(paises)
            print("✅ Países insertados correctamente.")
        
        # Insertar roles
        if Rol.query.count() == 0:
            roles = [
                Rol(nombre='Administrador', created_at=datetime.now(), updated_at=datetime.now()),
                Rol(nombre='Operario', created_at=datetime.now(), updated_at=datetime.now()),
                Rol(nombre='Supervisor', created_at=datetime.now(), updated_at=datetime.now()),
            ]
            db.session.bulk_save_objects(roles)
            print("✅ Roles insertados correctamente.")
        
        # Insertar usuarios
        if Usuario.query.count() == 0:
            usuarios = [
                Usuario(
                    documento='12345678', 
                    contrasena='$2b$12$WK/m7UiPnx0M5WK0aTu4YeQTKiflE8btM8638rTTYjb/hDI32l3rK',  # password: admin123
                    nombres='Admin', 
                    apellidos='Sistema', 
                    telefono='300-123-4567', 
                    email='admin@parqueadero.com', 
                    direccion='Calle Principal 123', 
                    ciudad='Bogotá', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    rol_id=1
                ),
                Usuario(
                    documento='87654321', 
                    contrasena='$2b$12$WK/m7UiPnx0M5WK0aTu4YeQTKiflE8btM8638rTTYjb/hDI32l3rK',  # password: admin123
                    nombres='Operario', 
                    apellidos='Prueba', 
                    telefono='300-987-6543', 
                    email='operario@parqueadero.com', 
                    direccion='Calle Secundaria 456', 
                    ciudad='Medellín', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    rol_id=2
                ),
            ]
            db.session.bulk_save_objects(usuarios)
            print("✅ Usuarios insertados correctamente.")
            print("   Usuario: admin@parqueadero.com / Contraseña: admin123")
        
        # Insertar parqueaderos
        if Parqueadero.query.count() == 0:
            parqueaderos = [
                Parqueadero(
                    rut='900123456-1', 
                    nombre='Parqueadero Central', 
                    direccion='Carrera 7 #32-16', 
                    telefono='601-234-5678', 
                    email='central@parqueadero.com', 
                    ciudad='Bogotá', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    pais_id=1
                ),
                Parqueadero(
                    rut='900987654-2', 
                    nombre='Parqueadero Norte', 
                    direccion='Calle 100 #15-30', 
                    telefono='601-345-6789', 
                    email='norte@parqueadero.com', 
                    ciudad='Bogotá', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    pais_id=1
                ),
            ]
            db.session.bulk_save_objects(parqueaderos)
            print("✅ Parqueaderos insertados correctamente.")
        
        # Insertar tipos de vehículo
        if VehiculoTipo.query.count() == 0:
            tipos_vehiculo = [
                VehiculoTipo(nombre='Automóvil', created_at=datetime.now(), updated_at=datetime.now()),
                VehiculoTipo(nombre='Motocicleta', created_at=datetime.now(), updated_at=datetime.now()),
                VehiculoTipo(nombre='Camioneta', created_at=datetime.now(), updated_at=datetime.now()),
                VehiculoTipo(nombre='Bicicleta', created_at=datetime.now(), updated_at=datetime.now()),
            ]
            db.session.bulk_save_objects(tipos_vehiculo)
            print("✅ Tipos de vehículo insertados correctamente.")
        
        # Insertar medios de pago
        if MedioPago.query.count() == 0:
            medios_pago = [
                MedioPago(nombre='Efectivo', created_at=datetime.now(), updated_at=datetime.now()),
                MedioPago(nombre='Tarjeta Débito', created_at=datetime.now(), updated_at=datetime.now()),
                MedioPago(nombre='Tarjeta Crédito', created_at=datetime.now(), updated_at=datetime.now()),
                MedioPago(nombre='Transferencia', created_at=datetime.now(), updated_at=datetime.now()),
            ]
            db.session.bulk_save_objects(medios_pago)
            print("✅ Medios de pago insertados correctamente.")
        
        # Insertar tipos de tarifa
        if TarifaTipo.query.count() == 0:
            tarifas_tipo = [
                TarifaTipo(nombre='Por Hora', unidad=1, created_at=datetime.now(), updated_at=datetime.now()),
                TarifaTipo(nombre='Por Día', unidad=24, created_at=datetime.now(), updated_at=datetime.now()),
                TarifaTipo(nombre='Por Mes', unidad=720, created_at=datetime.now(), updated_at=datetime.now()),
            ]
            db.session.bulk_save_objects(tarifas_tipo)
            print("✅ Tipos de tarifa insertados correctamente.")
        
        # Insertar tarifas
        if Tarifa.query.count() == 0:
            tarifas = [
                Tarifa(nombre='Hora Automóvil', costo=2000, created_at=datetime.now(), updated_at=datetime.now(), tarifa_tipo_id=1),
                Tarifa(nombre='Hora Motocicleta', costo=1000, created_at=datetime.now(), updated_at=datetime.now(), tarifa_tipo_id=1),
                Tarifa(nombre='Día Automóvil', costo=15000, created_at=datetime.now(), updated_at=datetime.now(), tarifa_tipo_id=2),
                Tarifa(nombre='Mes Automóvil', costo=200000, created_at=datetime.now(), updated_at=datetime.now(), tarifa_tipo_id=3),
            ]
            db.session.bulk_save_objects(tarifas)
            print("✅ Tarifas insertadas correctamente.")
        
        # Insertar clientes
        if Cliente.query.count() == 0:
            clientes = [
                Cliente(
                    documento='1234567890', 
                    nombres='Juan', 
                    apellidos='Pérez', 
                    telefono='300-111-2222', 
                    email='juan.perez@email.com', 
                    direccion='Calle 80 #10-15', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    parqueadero_id=1
                ),
                Cliente(
                    documento='0987654321', 
                    nombres='María', 
                    apellidos='García', 
                    telefono='300-333-4444', 
                    email='maria.garcia@email.com', 
                    direccion='Carrera 15 #45-20', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    parqueadero_id=1
                ),
            ]
            db.session.bulk_save_objects(clientes)
            print("✅ Clientes insertados correctamente.")
        
        # Insertar sedes
        if Sede.query.count() == 0:
            sedes = [
                Sede(
                    nombre='Sede Principal', 
                    direccion='Carrera 7 #32-16', 
                    telefono='601-234-5678', 
                    email='sede1@parqueadero.com', 
                    ciudad='Bogotá', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    parqueadero_id=1, 
                    usuario_id=1
                ),
            ]
            db.session.bulk_save_objects(sedes)
            print("✅ Sedes insertadas correctamente.")
        
        # Insertar módulos
        if Modulo.query.count() == 0:
            modulos = [
                Modulo(
                    nombre='Módulo A', 
                    habilitado=True, 
                    descripcion='Módulo principal para automóviles', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    sede_id=1
                ),
                Modulo(
                    nombre='Módulo B', 
                    habilitado=True, 
                    descripcion='Módulo para motocicletas', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    sede_id=1
                ),
            ]
            db.session.bulk_save_objects(modulos)
            print("✅ Módulos insertados correctamente.")
        
        # Insertar vehículos
        if Vehiculo.query.count() == 0:
            vehiculos = [
                Vehiculo(
                    placa='ABC123', 
                    marca='Toyota', 
                    modelo='Corolla', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    vehiculo_tipo_id=1, 
                    cliente_id=1
                ),
                Vehiculo(
                    placa='XYZ789', 
                    marca='Honda', 
                    modelo='CBR', 
                    created_at=datetime.now(), 
                    updated_at=datetime.now(), 
                    vehiculo_tipo_id=2, 
                    cliente_id=2
                ),
            ]
            db.session.bulk_save_objects(vehiculos)
            print("✅ Vehículos insertados correctamente.")
        
        # Insertar periodicidades
        if Periodicidad.query.count() == 0:
            periodicidades = [
                Periodicidad(nombre='Diaria', dias=1),
                Periodicidad(nombre='Semanal', dias=7),
                Periodicidad(nombre='Mensual', dias=30),
            ]
            db.session.bulk_save_objects(periodicidades)
            print("✅ Periodicidades insertadas correctamente.")
        
        # Confirmar cambios
        db.session.commit()
        
        print("\n🎉 ¡Base de datos inicializada correctamente!")
        print("\n📋 Resumen de datos insertados:")
        print(f"   - Países: {Pais.query.count()}")
        print(f"   - Roles: {Rol.query.count()}")
        print(f"   - Usuarios: {Usuario.query.count()}")
        print(f"   - Parqueaderos: {Parqueadero.query.count()}")
        print(f"   - Tipos de vehículo: {VehiculoTipo.query.count()}")
        print(f"   - Medios de pago: {MedioPago.query.count()}")
        print(f"   - Tipos de tarifa: {TarifaTipo.query.count()}")
        print(f"   - Tarifas: {Tarifa.query.count()}")
        print(f"   - Clientes: {Cliente.query.count()}")
        print(f"   - Sedes: {Sede.query.count()}")
        print(f"   - Módulos: {Modulo.query.count()}")
        print(f"   - Vehículos: {Vehiculo.query.count()}")
        print(f"   - Periodicidades: {Periodicidad.query.count()}")
        
        print("\n🔑 Credenciales de acceso:")
        print("   Email: admin@parqueadero.com")
        print("   Contraseña: admin123")
        print("\n🌐 Accede a la aplicación en: http://localhost")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")
        sys.exit(1)
