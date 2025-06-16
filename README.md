# ParqueaderoVirtual - Sistema de Gestión de Parqueaderos

Aplicación web para administrar múltiples sedes de parqueaderos, gestionar entradas y salidas de vehículos, calcular pagos, registrar usuarios, empleados y clientes. Cuenta con autenticación JWT, control de roles y un dashboard central para dueños y operarios. No requiere landing page, ya que está enfocado exclusivamente en el uso interno.

## Características Principales
- ✅ Múltiples sedes de parqueaderos configurables
- 👥 Gestión de usuarios con roles (admin, operario, etc.)
- 🧾 Control de ingresos, salidas y cobros automáticos
- 💰 Cálculo de tiempos de espera y dinero devuelto
- 🧑‍💼 Registro de clientes y trabajadores por sede
- 🔐 Autenticación JWT y sistema de permisos
- 📊 Dashboard funcional para monitoreo y control

## Tecnologías Utilizadas

### Backend
| Tecnología           | Uso                                 |
|----------------------|--------------------------------------|
| **Python Flask**     | Backend principal                    |
| **Flask-Login**      | Manejo de sesiones                   |
| **JWT**              | Autenticación segura                 |
| **SQLAlchemy**       | ORM para modelo de base de datos     |
| **SQLite**           | Base de datos local por defecto      |
| **Flask-Migrate**    | Migraciones de base de datos         |
| **Flask-Bcrypt**     | Encriptación de contraseñas          |

### Frontend
| Tecnología       | Uso                                |
|------------------|-------------------------------------|
| **Flask-WTF**    | Formularios seguros                 |
| **Bootstrap**    | Estilos del dashboard               |
| **Jinja2**       | Motor de plantillas para vistas     |

## Estructura del Proyecto
```bash
ParqueaderoVirtual/
├── app/               # Aplicación principal Flask
│   ├── models/        # Modelos SQLAlchemy
│   ├── routes/        # Rutas organizadas por recurso
│   ├── templates/     # Vistas Jinja2
│   ├── static/        # Archivos estáticos (CSS, JS)
├── migrations/        # Migraciones con Alembic
├── .env               # Variables de entorno
├── app.py             # Archivo de configuración principal
└── requirements.txt   # Dependencias del proyecto
```

## Vista previa del Proyecto

|                                  |                                 |
|----------------------------------|---------------------------------|
| ![Imagen 1](https://github.com/Juliandos/TiendaVirtual/blob/main/Imagenes/login.png)|![Imagen 2](https://github.com/Juliandos/TiendaVirtual/blob/main/Imagenes/dashboard.png)

|                                  |                                 |
|----------------------------------|---------------------------------|
| ![Imagen 2](https://github.com/Juliandos/TiendaVirtual/blob/main/Imagenes/Tienda%20Virtual.png) | ![Imagen 2](https://github.com/Juliandos/TiendaVirtual/blob/main/Imagenes/Carrito.png) |

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/Juliandos/Parqueadero.git
cd Parqueadero
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pipenv shell
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear un archivo .env en la raíz del proyecto:
```bash
SECRET_KEY=clave_secreta
DATABASE_URL=sqlite:///parqueadero.db
JWT_SECRET_KEY=mi_clave_jwt
```

### 4. Inicializar la base de datos
```bash
flask db init
flask db migrate -m "init"
flask db upgrade
```

### 5. Ejecutar el servidor
```bash
pipenv shell
pipenv run start
```

*Hecho con :heart: por [Julian Ortega](https://github.com/Juliandos).*
