# Extrae y prepara los datos de la latencia

import pandas as pd
import json
import os

# Define la ruta al directorio donde se encuentran tus archivos .jl
directorio = '/Users/andrew/Desktop/ETSIT 23-24/TFG/Dataset/ping'

# Prepara una lista para almacenar los datos de latencia
datos_latencia = []

# Recorre todos los archivos en el directorio que terminen en .jl
for archivo in os.listdir(directorio):
    if archivo.endswith('.jl'):
        with open(os.path.join(directorio, archivo), 'r') as f:
            for linea in f:
                datos = json.loads(linea)
                # Extrae los datos relevantes: timestamp, IP de respuesta y tiempo de latencia
                datos_latencia.append({
                    'timestamp': pd.to_datetime(datos['timestamp'], unit='s'),
                    'response_ip': datos['response_ip'],
                    'time_ms': datos['time_ms']
                })

# Crea un DataFrame de Pandas con los datos recopilados
df_latencia = pd.DataFrame(datos_latencia)

# Guarda el DataFrame como un archivo CSV
df_latencia.to_csv('laten_data.csv', index=False)

