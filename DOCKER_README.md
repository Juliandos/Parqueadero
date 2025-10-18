# 🐳 Dockerización - Sistema de Parqueadero

Este proyecto ha sido dockerizado para facilitar el despliegue en cualquier servidor VPS.

## 📁 Archivos de Dockerización

### Archivos principales:
- `Dockerfile` - Configuración de la imagen de la aplicación
- `docker-compose.yml` - Orquestación de servicios (app + nginx)
- `.dockerignore` - Archivos a excluir del build
- `env.example` - Plantilla de variables de entorno
- `deploy.sh` - Script automatizado de despliegue
- `init-db.py` - Script para inicializar la base de datos

### Configuración de Nginx:
- `nginx/nginx.conf` - Configuración del proxy reverso

## 🚀 Inicio Rápido

### 1. Preparar el entorno:
```bash
# Copiar variables de entorno
cp env.example .env

# Editar configuración (IMPORTANTE: cambiar SECRET_KEY)
nano .env
```

### 2. Ejecutar con Docker Compose:
```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 3. Inicializar base de datos:
```bash
# Ejecutar script de inicialización
python init-db.py
```

### 4. Acceder a la aplicación:
- **URL**: http://localhost
- **Usuario**: admin@parqueadero.com
- **Contraseña**: admin123

## 🛠️ Script de Despliegue

Usa el script `deploy.sh` para automatizar tareas comunes:

```bash
# Hacer ejecutable (en Linux/Mac)
chmod +x deploy.sh

# Comandos disponibles
./deploy.sh start      # Iniciar aplicación
./deploy.sh stop       # Detener aplicación
./deploy.sh restart    # Reiniciar aplicación
./deploy.sh update     # Actualizar aplicación
./deploy.sh logs       # Ver logs en tiempo real
./deploy.sh backup     # Crear backup
./deploy.sh status     # Ver estado de servicios
./deploy.sh help       # Mostrar ayuda
```

## 🔧 Configuración

### Variables de Entorno (.env):
```env
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
FLASK_ENV=production
FLASK_APP=main.py
SQLALCHEMY_DATABASE=sqlite:////app/data/app.db
LOG_LEVEL=INFO
DOMAIN=tu-dominio.com
```

### Puertos:
- **80**: Nginx (HTTP)
- **443**: Nginx (HTTPS, si está configurado)
- **5000**: Aplicación Flask (interno)

### Volúmenes:
- `./data` → `/app/data` (Base de datos)
- `./logs` → `/app/logs` (Logs de aplicación)

## 📊 Estructura de Servicios

```
┌─────────────────┐    ┌─────────────────┐
│     Nginx       │────│   Flask App     │
│  (Proxy Reverso)│    │   (Puerto 5000) │
│   (Puerto 80)   │    │                 │
└─────────────────┘    └─────────────────┘
         │                       │
         │                       │
    ┌─────────┐            ┌─────────┐
    │ Cliente │            │  SQLite │
    │ (Puerto │            │   DB    │
    │   80)   │            │         │
    └─────────┘            └─────────┘
```

## 🔒 Seguridad

### Configuraciones incluidas:
- Headers de seguridad en Nginx
- Compresión gzip habilitada
- Timeouts configurados
- Proxy reverso para ocultar la aplicación

### Para producción:
1. Cambiar `SECRET_KEY` por una clave segura
2. Configurar HTTPS con certificados SSL
3. Configurar firewall
4. Usar base de datos externa (PostgreSQL)

## 📈 Monitoreo

### Ver logs:
```bash
# Logs de la aplicación
docker-compose logs -f app

# Logs de Nginx
docker-compose logs -f nginx

# Todos los logs
docker-compose logs -f
```

### Verificar estado:
```bash
# Estado de contenedores
docker-compose ps

# Uso de recursos
docker stats
```

## 🔄 Backup y Restauración

### Backup automático:
```bash
./deploy.sh backup
```

### Backup manual:
```bash
# Backup completo
tar -czf backup-$(date +%Y%m%d).tar.gz data/ .env

# Solo base de datos
cp data/app.db data/app.db.backup.$(date +%Y%m%d_%H%M%S)
```

## 🐛 Resolución de Problemas

### La aplicación no inicia:
```bash
# Ver logs detallados
docker-compose logs app

# Verificar configuración
docker-compose config

# Reconstruir imagen
docker-compose build --no-cache
```

### Problemas de permisos:
```bash
# Verificar permisos
ls -la data/

# Corregir permisos
sudo chown -R 1000:1000 data/ logs/
```

### Problemas de red:
```bash
# Verificar conectividad
docker-compose exec app ping nginx

# Verificar puertos
netstat -tlnp | grep :80
```

## 🔧 Comandos Docker Útiles

```bash
# Limpiar sistema Docker
docker system prune -a

# Ver imágenes
docker images

# Ver contenedores
docker ps -a

# Acceder al contenedor
docker-compose exec app bash

# Reiniciar solo un servicio
docker-compose restart app
```

## 📝 Notas Importantes

1. **Primera ejecución**: Ejecuta `python init-db.py` después del primer despliegue
2. **Backup**: Haz backup regular de la carpeta `data/`
3. **Logs**: Los logs se almacenan en `logs/`
4. **SSL**: Para HTTPS, configura certificados en `nginx/ssl/`
5. **Dominio**: Actualiza `DOMAIN` en `.env` para tu dominio

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs: `./deploy.sh logs`
2. Verifica la configuración: `docker-compose config`
3. Consulta la guía completa: `DEPLOYMENT.md`

---

¡Tu aplicación de parqueadero está lista para producción! 🚗✨
