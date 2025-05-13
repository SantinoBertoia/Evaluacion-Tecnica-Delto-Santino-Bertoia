FROM python:3.10-slim

WORKDIR /app

# Copiar los requisitos para instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para la base de datos
RUN mkdir -p data

# Ejecutar el bot
CMD ["python", "main.py"]