#!/bin/bash

# Script de despliegue para la aplicación de Parqueadero
# Uso: ./deploy.sh [start|stop|restart|update|logs|backup]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Sistema de Parqueadero${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor instala Docker primero."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
        exit 1
    fi
}

# Verificar si existe el archivo .env
check_env() {
    if [ ! -f ".env" ]; then
        print_warning "Archivo .env no encontrado. Creando desde env.example..."
        if [ -f "env.example" ]; then
            cp env.example .env
            print_warning "Por favor edita el archivo .env con tus configuraciones antes de continuar."
            print_warning "Especialmente cambia SECRET_KEY por una clave segura."
            exit 1
        else
            print_error "Archivo env.example no encontrado."
            exit 1
        fi
    fi
}

# Crear directorios necesarios
create_directories() {
    print_message "Creando directorios necesarios..."
    mkdir -p data logs nginx/ssl
    chmod 755 data logs
    chmod 700 nginx/ssl
}

# Función para iniciar la aplicación
start_app() {
    print_header
    print_message "Iniciando la aplicación de Parqueadero..."
    
    check_docker
    check_env
    create_directories
    
    print_message "Construyendo imágenes Docker..."
    docker-compose build
    
    print_message "Iniciando servicios..."
    docker-compose up -d
    
    print_message "Esperando que los servicios estén listos..."
    sleep 10
    
    # Verificar que los contenedores estén ejecutándose
    if docker-compose ps | grep -q "Up"; then
        print_message "✅ Aplicación iniciada correctamente!"
        print_message "🌐 Accede a: http://localhost"
        print_message "📊 Para ver logs: ./deploy.sh logs"
    else
        print_error "❌ Error al iniciar la aplicación. Revisa los logs."
        docker-compose logs
        exit 1
    fi
}

# Función para detener la aplicación
stop_app() {
    print_header
    print_message "Deteniendo la aplicación..."
    docker-compose down
    print_message "✅ Aplicación detenida."
}

# Función para reiniciar la aplicación
restart_app() {
    print_header
    print_message "Reiniciando la aplicación..."
    docker-compose restart
    print_message "✅ Aplicación reiniciada."
}

# Función para actualizar la aplicación
update_app() {
    print_header
    print_message "Actualizando la aplicación..."
    
    # Hacer backup antes de actualizar
    backup_data
    
    print_message "Deteniendo servicios..."
    docker-compose down
    
    print_message "Construyendo nuevas imágenes..."
    docker-compose build --no-cache
    
    print_message "Iniciando servicios actualizados..."
    docker-compose up -d
    
    print_message "✅ Aplicación actualizada correctamente!"
}

# Función para mostrar logs
show_logs() {
    print_header
    print_message "Mostrando logs de la aplicación..."
    docker-compose logs -f
}

# Función para hacer backup
backup_data() {
    print_header
    print_message "Creando backup de datos..."
    
    BACKUP_DIR="backups"
    BACKUP_FILE="parqueadero-backup-$(date +%Y%m%d_%H%M%S).tar.gz"
    
    mkdir -p $BACKUP_DIR
    
    # Backup de datos y configuración
    tar -czf "$BACKUP_DIR/$BACKUP_FILE" data/ .env 2>/dev/null || true
    
    print_message "✅ Backup creado: $BACKUP_DIR/$BACKUP_FILE"
}

# Función para mostrar estado
show_status() {
    print_header
    print_message "Estado de los servicios:"
    docker-compose ps
    
    echo ""
    print_message "Uso de recursos:"
    docker stats --no-stream
}

# Función para mostrar ayuda
show_help() {
    print_header
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start     - Iniciar la aplicación"
    echo "  stop      - Detener la aplicación"
    echo "  restart   - Reiniciar la aplicación"
    echo "  update    - Actualizar la aplicación"
    echo "  logs      - Mostrar logs en tiempo real"
    echo "  backup    - Crear backup de datos"
    echo "  status    - Mostrar estado de servicios"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 start"
    echo "  $0 logs"
    echo "  $0 backup"
}

# Función principal
main() {
    case "${1:-help}" in
        start)
            start_app
            ;;
        stop)
            stop_app
            ;;
        restart)
            restart_app
            ;;
        update)
            update_app
            ;;
        logs)
            show_logs
            ;;
        backup)
            backup_data
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Comando no reconocido: $1"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
