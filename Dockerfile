FROM python:3.12

# directorio de trabajo
WORKDIR /app

# copia los archivos de requerimientos y la aplicación
COPY requirements.txt requirements.txt
COPY app/ .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de la aplicación
EXPOSE 5000

# Define el comando por defecto
CMD ["bash", "-c", "python app.py"]
