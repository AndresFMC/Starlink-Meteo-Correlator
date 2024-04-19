import matplotlib.pyplot as plt
import pandas as pd

# Carga los datos de velocidad de internet y los datos meteorológicos
speedtest_df = pd.read_csv('speedtest_data.csv')
meteo_df = pd.read_csv('meteo_data.csv')

# Convierte las columnas de tiempo a datetime
speedtest_df['Timestamp'] = pd.to_datetime(speedtest_df['Timestamp'])
meteo_df['date'] = pd.to_datetime(meteo_df['date'])

# Asegúrate de que los datos estén alineados temporalmente
meteo_df = meteo_df.set_index('date').resample('h').asfreq().reset_index()
speedtest_df = speedtest_df.set_index('Timestamp').resample('H').asfreq().reset_index()

# Calcula el promedio móvil del Throughput para suavizar las variaciones de corto plazo
speedtest_df['Throughput Moving Average'] = speedtest_df['Download Throughput'].rolling(window=24).mean()

# Prepara un gráfico combinado usando dos ejes Y
fig, ax1 = plt.subplots(figsize=(15, 7))

# Configura el eje Y primario para Throughput
color = 'tab:red'
ax1.set_xlabel('Time')
ax1.set_ylabel('Throughput (Mbps)', color=color)
ax1.plot(speedtest_df['Timestamp'], speedtest_df['Throughput Moving Average'], color=color, label='Throughput')
ax1.tick_params(axis='y', labelcolor=color)

# Crea un eje Y secundario compartiendo el mismo eje X para los datos meteorológicos
ax2 = ax1.twinx()

# Configura el eje secundario para precipitación
color = 'tab:blue'
ax2.set_ylabel('Precipitation (mm)', color=color)
ax2.bar(meteo_df['date'], meteo_df['precipitation'], color=color, alpha=0.3, label='Precipitation')
ax2.tick_params(axis='y', labelcolor=color)

# Configura otro eje Y secundario para nubosidad
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # Desplaza el eje de nubosidad a la derecha
color = 'tab:gray'
ax3.set_ylabel('Cloud Cover (%)', color=color)
ax3.fill_between(meteo_df['date'], meteo_df['cloud_cover'], color=color, alpha=0.3, label='Cloud Cover')
ax3.tick_params(axis='y', labelcolor=color)

# Añade leyendas
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax3.legend(loc='center right')

# Añade títulos y muestra la gráfica
plt.title('Internet Throughput, Precipitation, and Cloud Cover Over Time')
fig.tight_layout()
plt.show()
