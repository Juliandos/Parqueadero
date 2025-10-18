# Usar imagen base de Python 3.12 slim
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para la base de datos
RUN mkdir -p /app/data

# Exponer puerto 5000
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV SQLALCHEMY_DATABASE=sqlite:////app/data/app.db

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
