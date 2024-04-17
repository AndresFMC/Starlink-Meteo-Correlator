import json
import pandas as pd
import os
import glob

# Define el directorio donde se encuentran los archivos .jl
data_directory = '/Users/andrew/Desktop/ETSIT 23-24/TFG/Dataset/speed-test'

# Prepara una lista para almacenar los datos
data = []

# Lista todos los archivos .jl en el directorio
file_paths = glob.glob(os.path.join(data_directory, '*.jl'))

# Procesa cada archivo
for file_path in file_paths:
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Parsea el contenido JSON de la línea
                result = json.loads(line)

                # Verifica que todas las claves necesarias estén presentes
                if all(key in result for key in ['timestamp', 'ping', 'download', 'upload']):
                    # Extrae los datos de interés
                    timestamp = result['timestamp']
                    jitter = result['ping']['jitter']
                    latency = result['ping']['latency']
                    download_bandwidth = result['download']['bandwidth']  # bps
                    upload_bandwidth = result['upload']['bandwidth']  # bps
                    download_bytes = result['download']['bytes']
                    upload_bytes = result['upload']['bytes']
                    download_elapsed = result['download']['elapsed']  # ms
                    upload_elapsed = result['upload']['elapsed']  # ms
                    packet_loss = result.get('packetLoss', 0)

                    # Calcula el Throughput para download y upload (en Mbps)
                    download_throughput = (download_bytes * 8) / download_elapsed / 1024 / 1024  # Convert bytes to bits, then to Mbps
                    upload_throughput = (upload_bytes * 8) / upload_elapsed / 1024 / 1024  # Convert bytes to bits, then to Mbps

                    # Añade los datos a la lista
                    data.append([
                        timestamp, jitter, latency, download_bandwidth, upload_bandwidth,
                        download_throughput, upload_throughput, packet_loss
                    ])
                else:
                    print(f"Falta una clave en la línea: {line}")

            except json.JSONDecodeError as e:
                print(f"Error al parsear JSON: {e} en la línea: {line}")
            except KeyError as e:
                print(f"Clave no encontrada {e} en la línea: {line}")

# Crea un DataFrame con los datos recolectados
columns = [
    'Timestamp', 'Jitter', 'Latency', 'Download Bandwidth', 'Upload Bandwidth',
    'Download Throughput', 'Upload Throughput', 'Packet Loss'
]
df = pd.DataFrame(data, columns=columns)

# Convierte el campo 'Timestamp' a datetime para mejor manipulación
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Ordena el DataFrame por Timestamp
df = df.sort_values('Timestamp')

# Guarda los resultados en un archivo CSV para análisis posterior
output_file = 'speedtest_data.csv'
df.to_csv(output_file, index=False)

print(f"Archivo guardado: {output_file}")
