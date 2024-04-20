import pandas as pd
import matplotlib.pyplot as plt

# Cargando los datos de los archivos CSV
speedtest_data = pd.read_csv('speedtest_data.csv', parse_dates=['Timestamp'])
meteo_data = pd.read_csv('meteo_data.csv', parse_dates=['date'])

# Limpiando y preparando los datos
# Asegurando que los timestamps están en formato de fecha y hora correctos
speedtest_data['Timestamp'] = pd.to_datetime(speedtest_data['Timestamp'])
meteo_data['date'] = pd.to_datetime(meteo_data['date'])

# Resample de los datos meteorológicos para que coincidan con los tiempos de speedtest
meteo_data.set_index('date', inplace=True)
meteo_resampled = meteo_data.resample('15T').interpolate(method='time')  # interpolación cada 15 minutos

# Uniendo los datos mediante el índice de tiempo más cercano
combined_data = pd.merge_asof(speedtest_data.sort_values('Timestamp'),
                              meteo_resampled.reset_index().sort_values('date'),
                              left_on='Timestamp',
                              right_on='date',
                              direction='nearest')

# Visualizando las correlaciones
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
plt.scatter(combined_data['cloud_cover'], combined_data['Download Throughput'], alpha=0.5)
plt.title('Cloud Cover vs. Download Throughput')
plt.xlabel('Cloud Cover (%)')
plt.ylabel('Download Throughput (Gbps)')

plt.subplot(1, 2, 2)
plt.scatter(combined_data['rain'], combined_data['Download Throughput'], alpha=0.5)
plt.title('Rain vs. Download Throughput')
plt.xlabel('Rain (mm)')
plt.ylabel('Download Throughput (Gbps)')

plt.tight_layout()
plt.show()

# Calculando coeficientes de correlación
correlation_cloud_cover = combined_data['cloud_cover'].corr(combined_data['Download Throughput'])
correlation_rain = combined_data['rain'].corr(combined_data['Download Throughput'])

correlation_cloud_cover, correlation_rain

