FROM python:3.12

# directorio de trabajo
WORKDIR /app

# copia los archivos de requerimientos y la aplicación
COPY requirements.txt requirements.txt
COPY app/ .

# Copia wait-for-it.sh y establece permisos de ejecución
COPY wait-for-it/wait-for-it.sh wait-for-it/wait-for-it.sh
RUN chmod +x wait-for-it/wait-for-it.sh

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de la aplicación
EXPOSE 5000

# Define el comando por defecto
CMD ["bash", "-c", "./wait-for-it/wait-for-it.sh db:3306 -- python app.py"]
