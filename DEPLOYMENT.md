# Guía de Despliegue - Sistema de Parqueadero

Esta guía te ayudará a desplegar la aplicación de gestión de parqueaderos en un VPS usando Docker.

## Requisitos Previos

### En tu VPS:
- Ubuntu 20.04+ o similar
- Docker instalado
- Docker Compose instalado
- Acceso SSH al servidor
- Dominio configurado (opcional, para HTTPS)

### Instalación de Docker en Ubuntu:

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar el repositorio de Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar tu usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar la sesión o ejecutar:
newgrp docker
```

## Pasos de Despliegue

### 1. Preparar el Servidor

```bash
# Crear directorio para la aplicación
sudo mkdir -p /opt/parqueadero
cd /opt/parqueadero

# Crear usuario para la aplicación (opcional pero recomendado)
sudo useradd -r -s /bin/false parqueadero
sudo chown -R parqueadero:parqueadero /opt/parqueadero
```

### 2. Subir los Archivos

Sube todos los archivos del proyecto a `/opt/parqueadero/` en tu VPS. Puedes usar:

- **SCP**: `scp -r . usuario@tu-vps:/opt/parqueadero/`
- **Git**: Clonar el repositorio directamente en el servidor
- **SFTP**: Usar un cliente como FileZilla

### 3. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar las variables de entorno
nano .env
```

Configura las siguientes variables en `.env`:

```env
SECRET_KEY=tu_clave_secreta_muy_segura_y_larga_aqui
FLASK_ENV=production
FLASK_APP=main.py
SQLALCHEMY_DATABASE=sqlite:////app/data/app.db
LOG_LEVEL=INFO
DOMAIN=tu-dominio.com
```

**⚠️ IMPORTANTE**: Cambia `SECRET_KEY` por una clave segura. Puedes generar una con:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Crear Directorios Necesarios

```bash
# Crear directorios para datos persistentes
mkdir -p data logs nginx/ssl

# Establecer permisos correctos
chmod 755 data logs
chmod 700 nginx/ssl
```

### 5. Construir y Ejecutar la Aplicación

```bash
# Construir las imágenes
docker-compose build

# Ejecutar en segundo plano
docker-compose up -d

# Verificar que los contenedores estén ejecutándose
docker-compose ps
```

### 6. Verificar el Despliegue

```bash
# Ver logs de la aplicación
docker-compose logs -f app

# Ver logs de Nginx
docker-compose logs -f nginx

# Verificar que la aplicación responda
curl http://localhost
```

### 7. Configurar Firewall (Opcional)

```bash
# Instalar UFW si no está instalado
sudo apt install ufw

# Configurar reglas básicas
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Habilitar firewall
sudo ufw enable
```

## Configuración de HTTPS (Opcional)

### Usando Let's Encrypt con Certbot:

```bash
# Instalar Certbot
sudo apt install certbot

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com

# Copiar certificados al directorio de Nginx
sudo cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem nginx/ssl/key.pem

# Editar nginx.conf para habilitar HTTPS
nano nginx/nginx.conf
```

Descomenta y configura la sección HTTPS en `nginx/nginx.conf`.

## Comandos Útiles

### Gestión de la Aplicación:

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f

# Actualizar la aplicación
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Hacer backup de la base de datos
docker-compose exec app cp /app/data/app.db /app/data/app.db.backup.$(date +%Y%m%d_%H%M%S)
```

### Monitoreo:

```bash
# Ver uso de recursos
docker stats

# Ver estado de contenedores
docker-compose ps

# Acceder al contenedor de la aplicación
docker-compose exec app bash
```

## Resolución de Problemas

### La aplicación no inicia:
```bash
# Ver logs detallados
docker-compose logs app

# Verificar configuración
docker-compose config
```

### Problemas de permisos:
```bash
# Verificar permisos de archivos
ls -la data/

# Corregir permisos
sudo chown -R 1000:1000 data/ logs/
```

### Problemas de red:
```bash
# Verificar conectividad entre contenedores
docker-compose exec app ping nginx

# Verificar puertos
netstat -tlnp | grep :80
```

## Backup y Restauración

### Backup:
```bash
# Crear backup completo
tar -czf parqueadero-backup-$(date +%Y%m%d).tar.gz data/ logs/ .env

# Backup solo de base de datos
cp data/app.db data/app.db.backup.$(date +%Y%m%d_%H%M%S)
```

### Restauración:
```bash
# Restaurar desde backup completo
tar -xzf parqueadero-backup-YYYYMMDD.tar.gz

# Restaurar solo base de datos
cp data/app.db.backup.YYYYMMDD_HHMMSS data/app.db
```

## Mantenimiento

### Actualización de la aplicación:
1. Hacer backup de la base de datos
2. Detener servicios: `docker-compose down`
3. Actualizar código
4. Reconstruir: `docker-compose build --no-cache`
5. Iniciar: `docker-compose up -d`

### Limpieza de Docker:
```bash
# Limpiar imágenes no utilizadas
docker system prune -a

# Limpiar volúmenes no utilizados
docker volume prune
```

## Configuración de Dominio

Si tienes un dominio, configura los registros DNS:
- **A Record**: Apunta tu dominio a la IP del VPS
- **CNAME**: Para subdominios (opcional)

## Monitoreo y Logs

Los logs se almacenan en:
- Aplicación: `logs/app.log`
- Nginx: `logs/nginx.log`

Para monitoreo avanzado, considera usar herramientas como:
- Prometheus + Grafana
- ELK Stack
- Datadog

## Seguridad Adicional

1. **Cambiar puertos por defecto** si es necesario
2. **Configurar fail2ban** para protección contra ataques
3. **Usar un proxy reverso** como Cloudflare
4. **Implementar backup automático**
5. **Monitorear logs** regularmente

---

¡Tu aplicación de parqueadero debería estar funcionando correctamente en tu VPS! 🚗
