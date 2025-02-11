from datetime import datetime
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar configuración desde la clase
    app.config.from_object(Config) 

    db.init_app(app)

    from app import models  # Importar modelos

    with app.app_context():
        db.create_all()
        # seed_initial_data()

    from app.routes import routes  
    app.register_blueprint(routes)

    return app

def seed_initial_data():
    from app.models import VehiculoTipo, TarifaTipo, Tarifa, Modulo, Vehiculo, Parqueo, Punto, Redimir, Arrendamiento, Sede, Pais, Usuario, Rol, Periodicidad, Cliente, MedioPago, Parqueadero

    if VehiculoTipo.query.count() == 0:
        # Insertar datos en VehiculoTipo
        tipos_vehiculo = [
            VehiculoTipo(nombre='Motocicleta', created_at=datetime.strptime('11/29/2024', '%m/%d/%Y'), updated_at=datetime.strptime('7/25/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Automóvil', created_at=datetime.strptime('5/17/2024', '%m/%d/%Y'), updated_at=datetime.strptime('10/11/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Camioneta', created_at=datetime.strptime('12/16/2024', '%m/%d/%Y'), updated_at=datetime.strptime('8/11/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Camión', created_at=datetime.strptime('11/18/2024', '%m/%d/%Y'), updated_at=datetime.strptime('1/14/2025', '%m/%d/%Y')),
            VehiculoTipo(nombre='Móviles', created_at=datetime.strptime('5/25/2024', '%m/%d/%Y'), updated_at=datetime.strptime('3/7/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Bus', created_at=datetime.strptime('12/31/2024', '%m/%d/%Y'), updated_at=datetime.strptime('9/6/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Bicicleta', created_at=datetime.strptime('4/27/2024', '%m/%d/%Y'), updated_at=datetime.strptime('8/18/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Motocicleta Deportiva', created_at=datetime.strptime('4/27/2024', '%m/%d/%Y'), updated_at=datetime.strptime('5/25/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Automóvil Familiar', created_at=datetime.strptime('4/27/2024', '%m/%d/%Y'), updated_at=datetime.strptime('5/25/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Camioneta SUV', created_at=datetime.strptime('4/27/2024', '%m/%d/%Y'), updated_at=datetime.strptime('4/27/2024', '%m/%d/%Y')),
            VehiculoTipo(nombre='Camion Articulado', created_at=datetime.strptime('4/27/2024', '%m/%d/%Y'), updated_at=None),
        ]
        db.session.bulk_save_objects(tipos_vehiculo)
        print("✅ Datos iniciales de vehiculo_tipo cargados")

    if Rol.query.count() == 0:
        # Insertar datos en Rol
        roles = [
            Rol(nombre='Jefe', created_at=datetime.strptime('2024-12-01 00:00:00', '%Y-%m-%d %H:%M:%S'), updated_at=datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
            Rol(nombre='Administrador', created_at=datetime.strptime('2024-12-01 00:00:00', '%Y-%m-%d %H:%M:%S'), updated_at=datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
            Rol(nombre='Operario', created_at=datetime.strptime('2024-12-01 00:00:00', '%Y-%m-%d %H:%M:%S'), updated_at=datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
        ]
        db.session.bulk_save_objects(roles)
        print("✅ Datos iniciales de rol cargados")

    if Usuario.query.count() == 0:
        # Insertar datos en Usuario
        usuarios = [
            Usuario(documento='584-53-0773', contrasena='123456', nombres='Julian', apellidos='Petigrew', telefono='429-233-4414', email='julian@gmail.com', direccion='7 Northland Circle', ciudad='Río Grande', created_at=datetime.strptime('5/27/2024', '%m/%d/%Y'), updated_at=datetime.strptime('2/5/2025', '%m/%d/%Y'), rol_id=2),
            Usuario(documento='742-87-8089', contrasena='hE5}y">#<', nombres='Neils', apellidos='Levesque', telefono='254-498-1366', email='nlevesque1@canalblog.com', direccion='077 Mesta Alley', ciudad='Fresnes', created_at=datetime.strptime('9/26/2024', '%m/%d/%Y'), updated_at=datetime.strptime('7/22/2024', '%m/%d/%Y'), rol_id=2),
            Usuario(documento='688-93-3923', contrasena='aK2>ej*pKId61', nombres='Florette', apellidos='Docket', telefono='871-919-4896', email='fdocket2@blogspot.com', direccion='170 Eagle Crest Crossing', ciudad='Xiashan', created_at=datetime.strptime('3/26/2024', '%m/%d/%Y'), updated_at=datetime.strptime('9/14/2024', '%m/%d/%Y'), rol_id=2),
            Usuario(documento='812-93-0345', contrasena='vZ7{E)AU{k|Sj=Pw', nombres='Hinda', apellidos='Seaborne', telefono='100-274-5002', email='hseaborne3@163.com', direccion='6838 Becker Parkway', ciudad='Lau', created_at=datetime.strptime('11/21/2024', '%m/%d/%Y'), updated_at=datetime.strptime('1/27/2025', '%m/%d/%Y'), rol_id=2),
            Usuario(documento='197-64-5442', contrasena='dP8.25v}Yu8{', nombres='Jens', apellidos='Kerne', telefono='812-593-5940', email='jkerne4@tripod.com', direccion='5 Ilene Terrace', ciudad='Beitan', created_at=datetime.strptime('10/22/2024', '%m/%d/%Y'), updated_at=datetime.strptime('2/18/2024', '%m/%d/%Y'), rol_id=2),
        ]
        db.session.bulk_save_objects(usuarios)
        print("✅ Datos iniciales de usuario cargados")

    if Parqueadero.query.count() == 0:
        # Insertar datos en Parqueadero
        parqueaderos = [
            Parqueadero(rut='55-756-0644', nombre='P1', direccion='5678 Spaight Junction', telefono='266-538-1249', email='jandreazzi0@webmd.com', ciudad='Limbaan', created_at=datetime.strptime('7/13/2024', '%m/%d/%Y'), updated_at=datetime.strptime('11/8/2024', '%m/%d/%Y'), usuario_id=1, pais_id=1),
            Parqueadero(rut='91-912-1971', nombre='P2', direccion='4563 Becker Point', telefono='492-452-9778', email='preece1@berkeley.edu', ciudad='Bayt Wazan', created_at=datetime.strptime('6/25/2024', '%m/%d/%Y'), updated_at=datetime.strptime('5/14/2024', '%m/%d/%Y'), usuario_id=2, pais_id=2),
            Parqueadero(rut='96-436-9977', nombre='P3', direccion='48 Arizona Plaza', telefono='288-741-4898', email='mjermey2@google.co.jp', ciudad='Klimontów', created_at=datetime.strptime('9/13/2024', '%m/%d/%Y'), updated_at=datetime.strptime('6/17/2024', '%m/%d/%Y'), usuario_id=3, pais_id=2),
            Parqueadero(rut='12-435-1269', nombre='P4', direccion='8 Clove Street', telefono='568-868-4539', email='wlewins3@answers.com', ciudad='Osan', created_at=datetime.strptime('1/8/2025', '%m/%d/%Y'), updated_at=datetime.strptime('4/12/2024', '%m/%d/%Y'), usuario_id=4, pais_id=3),
            Parqueadero(rut='50-092-1403', nombre='P5', direccion='12 Karstens Center', telefono='207-539-6114', email='echomicz4@java.com', ciudad='Kedungbacin', created_at=datetime.strptime('5/6/2024', '%m/%d/%Y'), updated_at=datetime.strptime('9/7/2024', '%m/%d/%Y'), usuario_id=5, pais_id=4),
        ]
        db.session.bulk_save_objects(parqueaderos)
        print("✅ Datos iniciales de parqueadero cargados")

    if Cliente.query.count() == 0:
        # Insertar datos en Cliente
        clientes = [
            Cliente(documento='742743399-8', nombres='Shari', apellidos='Byk', telefono='406-976-5417', email='sbyk0@ow.ly', direccion='162 Golf Course Avenue', created_at=datetime.strptime('4/12/2024', '%m/%d/%Y'), updated_at=datetime.strptime('11/11/2024', '%m/%d/%Y'), parqueadero_id=1),
            Cliente(documento='575026071-2', nombres='Riley', apellidos='Drepp', telefono='278-953-7718', email='rdrepp1@dell.com', direccion='06 Shoshone Pass', created_at=datetime.strptime('6/20/2024', '%m/%d/%Y'), updated_at=datetime.strptime('9/12/2024', '%m/%d/%Y'), parqueadero_id=2),
            Cliente(documento='945392175-0', nombres='Joana', apellidos='Fulleylove', telefono='113-272-9725', email='jfulleylove2@howstuffworks.com', direccion='7507 5th Crossing', created_at=datetime.strptime('2/19/2024', '%m/%d/%Y'), updated_at=datetime.strptime('12/9/2024', '%m/%d/%Y'), parqueadero_id=2),
            Cliente(documento='757484835-1', nombres='Agna', apellidos='Arthey', telefono='406-988-5252', email='aarthey3@ebay.com', direccion='9592 Hoffman Circle', created_at=datetime.strptime('7/18/2024', '%m/%d/%Y'), updated_at=datetime.strptime('3/31/2024', '%m/%d/%Y'), parqueadero_id=3),
            Cliente(documento='915759852-5', nombres='Ricki', apellidos='Stapley', telefono='950-580-1646', email='rstapley4@barnesandnoble.com', direccion='9 Golden Leaf Place', created_at=datetime.strptime('9/15/2024', '%m/%d/%Y'), updated_at=datetime.strptime('2/25/2024', '%m/%d/%Y'), parqueadero_id=3),
        ]
        db.session.bulk_save_objects(clientes)
        print("✅ Datos iniciales de cliente cargados")

    if Sede.query.count() == 0:
        # Insertar datos en Sede
        sedes = [
            Sede(nombre='Norte', direccion='27 West Hill', telefono='993-467-7459', email='tpeggrem0@jimdo.com', ciudad='Inđija', created_at=datetime.strptime('10/9/2024', '%m/%d/%Y'), updated_at=datetime.strptime('9/8/2024', '%m/%d/%Y'), parqueadero_id=1, usuario_id=1),
            Sede(nombre='Sur', direccion='020 Browning Lane', telefono='113-437-7307', email='kviscovi1@epa.gov', ciudad='Wamba', created_at=datetime.strptime('7/8/2024', '%m/%d/%Y'), updated_at=datetime.strptime('8/11/2024', '%m/%d/%Y'), parqueadero_id=2, usuario_id=2),
            Sede(nombre='Este', direccion='087 Barby Street', telefono='745-611-4112', email='mavann2@quantcast.com', ciudad='Makuyuni', created_at=datetime.strptime('8/10/2024', '%m/%d/%Y'), updated_at=datetime.strptime('8/25/2024', '%m/%d/%Y'), parqueadero_id=3, usuario_id=3),
            Sede(nombre='Oste', direccion='16013 Veith Pass', telefono='930-517-4121', email='cclineck3@google.it', ciudad='Huangshapu', created_at=datetime.strptime('7/1/2024', '%m/%d/%Y'), updated_at=datetime.strptime('4/22/2024', '%m/%d/%Y'), parqueadero_id=4, usuario_id=4),
            Sede(nombre='O Ésta', direccion='9 Pearson Hill', telefono='822-895-1783', email='fvogelein4@google.ca', ciudad='Troyits’ke', created_at=datetime.strptime('1/10/2025', '%m/%d/%Y'), updated_at=datetime.strptime('1/22/2025', '%m/%d/%Y'), parqueadero_id=5, usuario_id=5),
        ]
        db.session.bulk_save_objects(sedes)
        print("✅ Datos iniciales de sede cargados")

    if Modulo.query.count() == 0:
        # Insertar datos en Modulo
        modulos = [
            Modulo(nombre='M1', habilitado=True, descripcion='ultrices posuere cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam porttitor lacus', created_at=datetime.strptime('2/8/2025', '%m/%d/%Y'), updated_at=datetime.strptime('12/2/2024', '%m/%d/%Y'), sede_id=2),
            Modulo(nombre='M2', habilitado=False, descripcion='mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat morbi a ipsum integer a', created_at=datetime.strptime('10/22/2024', '%m/%d/%Y'), updated_at=datetime.strptime('4/3/2024', '%m/%d/%Y'), sede_id=3),
            Modulo(nombre='M3', habilitado=False, descripcion='neque sapien placerat ante nulla justo aliquam quis turpis eget elit sodales scelerisque mauris sit', created_at=datetime.strptime('5/23/2024', '%m/%d/%Y'), updated_at=datetime.strptime('3/4/2024', '%m/%d/%Y'), sede_id=4),
            Modulo(nombre='M4', habilitado=True, descripcion='nulla ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo pellentesque viverra pede ac diam cras pellentesque', created_at=datetime.strptime('4/25/2024', '%m/%d/%Y'), updated_at=datetime.strptime('3/1/2024', '%m/%d/%Y'), sede_id=5),
            Modulo(nombre='Amargo', habilitado=False, descripcion='non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit', created_at=datetime.strptime('8/31/2024', '%m/%d/%Y'), updated_at=datetime.strptime('1/2/2025', '%m/%d/%Y'), sede_id=6),
        ]
        db.session.bulk_save_objects(modulos)
        print("✅ Datos iniciales de modulo cargados")

    if Pais.query.count() == 0:
        paises = [
            Pais(id=1, nombre='Colombia', created_at=datetime(2024, 1, 27), updated_at=datetime(2025, 1, 4)),
            Pais(id=2, nombre='Vietnam', created_at=datetime(2024, 5, 28), updated_at=datetime(2024, 7, 6)),
            Pais(id=3, nombre='Brazil', created_at=datetime(2024, 2, 13), updated_at=datetime(2024, 2, 6)),
            Pais(id=4, nombre='Russia', created_at=datetime(2024, 6, 12), updated_at=datetime(2024, 12, 28)),
            Pais(id=5, nombre='Mauritius', created_at=datetime(2025, 1, 1), updated_at=datetime(2024, 6, 5)),
            Pais(id=6, nombre='Canada', created_at=datetime(2024, 2, 9), updated_at=datetime(2024, 5, 19)),
            Pais(id=7, nombre='China', created_at=datetime(2024, 5, 6), updated_at=datetime(2024, 3, 14)),
            Pais(id=8, nombre='Ukraine', created_at=datetime(2024, 9, 11), updated_at=datetime(2024, 1, 10)),
            Pais(id=9, nombre='Portugal', created_at=datetime(2024, 11, 3), updated_at=datetime(2024, 12, 19)),
            Pais(id=10, nombre='China', created_at=datetime(2024, 6, 4), updated_at=datetime(2024, 8, 25)),
        ]

        db.session.bulk_save_objects(paises)
        print("✅ Países insertados correctamente.")

    if MedioPago.query.count() == 0:

        medios_pago = [
            MedioPago(id=1, nombre='Cheques', created_at=datetime(2024, 11, 29), updated_at=datetime(2024, 7, 25)),
            MedioPago(id=2, nombre='Débito', created_at=datetime(2024, 5, 17), updated_at=datetime(2024, 10, 11)),
            MedioPago(id=3, nombre='Crédito', created_at=datetime(2024, 12, 16), updated_at=datetime(2024, 8, 11)),
            MedioPago(id=4, nombre='Móviles', created_at=datetime(2024, 11, 18), updated_at=datetime(2025, 1, 14)),
            MedioPago(id=5, nombre='Transferencia', created_at=datetime(2024, 5, 25), updated_at=datetime(2024, 3, 7)),
            MedioPago(id=6, nombre='Paypal', created_at=datetime(2024, 12, 31), updated_at=datetime(2024, 9, 6)),
            MedioPago(id=7, nombre='Otro', created_at=datetime(2024, 4, 27), updated_at=datetime(2024, 8, 18)),
        ]

        db.session.bulk_save_objects(medios_pago)
        print("✅ Medios de pago insertados correctamente.")

    if TarifaTipo.query.count() == 0:
        tarifas_tipo = [
            TarifaTipo(nombre='Joice', unidad=1, created_at=datetime.strptime('11/28/2024', '%m/%d/%Y'), updated_at=datetime.strptime('11/14/2024', '%m/%d/%Y')),
            TarifaTipo(nombre='Lela', unidad=2, created_at=datetime.strptime('5/15/2024', '%m/%d/%Y'), updated_at=datetime.strptime('9/30/2024', '%m/%d/%Y')),
            TarifaTipo(nombre='Salvatore', unidad=0, created_at=datetime.strptime('8/29/2024', '%m/%d/%Y'), updated_at=datetime.strptime('1/19/2025', '%m/%d/%Y')),
            TarifaTipo(nombre='Iggie', unidad=0, created_at=datetime.strptime('3/3/2024', '%m/%d/%Y'), updated_at=datetime.strptime('5/13/2024', '%m/%d/%Y')),
            TarifaTipo(nombre='Agustin', unidad=1, created_at=datetime.strptime('4/29/2024', '%m/%d/%Y'), updated_at=datetime.strptime('5/7/2024', '%m/%d/%Y')),
        ]
        db.session.bulk_save_objects(tarifas_tipo)
        print("✅ Tipos de Tarifa insertados correctamente.")

    db.session.commit()
    print("✅ Todos los datos iniciales han sido cargados exitosamente.")