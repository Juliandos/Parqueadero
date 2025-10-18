# 🚀 Despliegue en VPS - Sistema de Parqueadero

Guía paso a paso para desplegar la aplicación de parqueadero en un VPS.

## 📋 Checklist Pre-Despliegue

- [ ] VPS con Ubuntu 20.04+ configurado
- [ ] Acceso SSH al servidor
- [ ] Dominio configurado (opcional)
- [ ] Archivos del proyecto listos

## 🛠️ Paso 1: Preparar el VPS

### Conectar al servidor:
```bash
ssh usuario@tu-vps-ip
```

### Actualizar el sistema:
```bash
sudo apt update && sudo apt upgrade -y
```

### Instalar Docker:
```bash
# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Agregar clave GPG de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

## 📁 Paso 2: Subir Archivos al VPS

### Opción A: Usando SCP
```bash
# Desde tu máquina local
scp -r . usuario@tu-vps-ip:/opt/parqueadero/
```

### Opción B: Usando Git
```bash
# En el VPS
sudo mkdir -p /opt/parqueadero
cd /opt/parqueadero
git clone tu-repositorio .
```

### Opción C: Usando SFTP
Usa un cliente como FileZilla para subir todos los archivos.

## ⚙️ Paso 3: Configurar la Aplicación

### Crear directorio y configurar permisos:
```bash
sudo mkdir -p /opt/parqueadero
cd /opt/parqueadero

# Configurar permisos
sudo chown -R $USER:$USER /opt/parqueadero
chmod +x deploy.sh
chmod +x init-db.py
```

### Configurar variables de entorno:
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar configuración
nano .env
```

**Configuración mínima en .env:**
```env
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_cambiar
FLASK_ENV=production
FLASK_APP=main.py
SQLALCHEMY_DATABASE=sqlite:////app/data/app.db
LOG_LEVEL=INFO
DOMAIN=tu-dominio.com
```

**Generar SECRET_KEY segura:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Paso 4: Desplegar la Aplicación

### Usar el script automatizado:
```bash
# Iniciar aplicación
./deploy.sh start
```

### O manualmente:
```bash
# Crear directorios necesarios
mkdir -p data logs nginx/ssl

# Construir y ejecutar
docker-compose build
docker-compose up -d

# Verificar estado
docker-compose ps
```

## 🗄️ Paso 5: Inicializar Base de Datos

```bash
# Ejecutar script de inicialización
python3 init-db.py
```

Esto creará:
- Usuarios de prueba
- Datos iniciales
- Estructura de base de datos

**Credenciales por defecto:**
- Email: `admin@parqueadero.com`
- Contraseña: `admin123`

## 🔒 Paso 6: Configurar Firewall

```bash
# Instalar UFW
sudo apt install ufw

# Configurar reglas
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Habilitar firewall
sudo ufw enable
```

## 🌐 Paso 7: Configurar Dominio (Opcional)

### Si tienes un dominio:

1. **Configurar DNS:**
   - A Record: `tu-dominio.com` → IP del VPS
   - CNAME: `www.tu-dominio.com` → `tu-dominio.com`

2. **Configurar HTTPS con Let's Encrypt:**
```bash
# Instalar Certbot
sudo apt install certbot

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com

# Copiar certificados
sudo cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem nginx/ssl/key.pem

# Editar nginx.conf para habilitar HTTPS
nano nginx/nginx.conf
```

3. **Actualizar .env:**
```env
DOMAIN=tu-dominio.com
```

## ✅ Paso 8: Verificar Despliegue

### Verificar que todo funcione:
```bash
# Ver logs
./deploy.sh logs

# Ver estado
./deploy.sh status

# Probar acceso
curl http://tu-vps-ip
# o
curl http://tu-dominio.com
```

### Acceder a la aplicación:
- **URL**: `http://tu-vps-ip` o `http://tu-dominio.com`
- **Usuario**: `admin@parqueadero.com`
- **Contraseña**: `admin123`

## 🔧 Comandos de Mantenimiento

### Gestión diaria:
```bash
# Ver logs
./deploy.sh logs

# Reiniciar aplicación
./deploy.sh restart

# Crear backup
./deploy.sh backup

# Ver estado
./deploy.sh status
```

### Actualización:
```bash
# Hacer backup
./deploy.sh backup

# Actualizar aplicación
./deploy.sh update
```

### Limpieza:
```bash
# Limpiar Docker
docker system prune -a

# Limpiar logs antiguos
find logs/ -name "*.log" -mtime +30 -delete
```

## 📊 Monitoreo

### Verificar recursos:
```bash
# Uso de CPU y memoria
htop

# Uso de Docker
docker stats

# Espacio en disco
df -h
```

### Logs importantes:
```bash
# Logs de aplicación
tail -f logs/app.log

# Logs de Nginx
tail -f logs/nginx.log

# Logs del sistema
sudo journalctl -f
```

## 🆘 Resolución de Problemas

### La aplicación no inicia:
```bash
# Ver logs detallados
docker-compose logs app

# Verificar configuración
docker-compose config

# Reconstruir
docker-compose build --no-cache
```

### Error de permisos:
```bash
# Corregir permisos
sudo chown -R $USER:$USER /opt/parqueadero
chmod -R 755 data/ logs/
```

### Problemas de red:
```bash
# Verificar puertos
sudo netstat -tlnp | grep :80

# Verificar firewall
sudo ufw status
```

### Base de datos corrupta:
```bash
# Restaurar desde backup
cp data/app.db.backup.YYYYMMDD_HHMMSS data/app.db

# O reinicializar
rm data/app.db
python3 init-db.py
```

## 🔄 Backup Automático

### Crear script de backup automático:
```bash
# Crear script
nano /opt/parqueadero/backup-auto.sh
```

**Contenido del script:**
```bash
#!/bin/bash
cd /opt/parqueadero
./deploy.sh backup

# Limpiar backups antiguos (más de 30 días)
find backups/ -name "*.tar.gz" -mtime +30 -delete

# Enviar notificación (opcional)
echo "Backup completado: $(date)" | mail -s "Backup Parqueadero" tu-email@ejemplo.com
```

### Programar con cron:
```bash
# Editar crontab
crontab -e

# Agregar línea para backup diario a las 2 AM
0 2 * * * /opt/parqueadero/backup-auto.sh
```

## 📈 Optimizaciones para Producción

### Usar docker-compose.prod.yml:
```bash
# Para producción con más recursos
docker-compose -f docker-compose.prod.yml up -d
```

### Configurar swap (si es necesario):
```bash
# Crear archivo de swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Hacer permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Optimizar Nginx:
```bash
# Editar configuración
nano nginx/nginx.conf

# Ajustar worker_processes según CPU
worker_processes auto;
```

## 🎯 Checklist Post-Despliegue

- [ ] Aplicación accesible desde navegador
- [ ] Login funciona correctamente
- [ ] Base de datos inicializada
- [ ] Firewall configurado
- [ ] Backup automático configurado
- [ ] Monitoreo básico funcionando
- [ ] HTTPS configurado (si aplica)
- [ ] Dominio apuntando correctamente

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `./deploy.sh logs`
2. Verifica el estado: `./deploy.sh status`
3. Consulta la documentación: `DEPLOYMENT.md`
4. Revisa la configuración: `docker-compose config`

---

¡Tu aplicación de parqueadero está lista para producción! 🚗✨

**URL de acceso**: `http://tu-vps-ip` o `http://tu-dominio.com`
**Usuario**: `admin@parqueadero.com`
**Contraseña**: `admin123`
