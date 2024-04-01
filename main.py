import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Asumiendo que ya has cargado tu hourly_dataframe desde 'meteo_data.json' o 'meteo_data.csv'
hourly_dataframe = pd.read_csv('meteo_data.csv', parse_dates=['date'])

# Filtrar el DataFrame para el rango de fechas deseado
start_date = "2021-12-20"
end_date = "2022-09-08"
mask = (hourly_dataframe['date'] >= start_date) & (hourly_dataframe['date'] <= end_date)
filtered_df = hourly_dataframe.loc[mask]

# Crear la figura y los ejes para el gráfico
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
# Configurar el eje Y para las precipitaciones
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Precipitaciones (mm)', color=color)
ax1.plot(filtered_df['date'], filtered_df['precipitation'], color=color, label='Precipitaciones')
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje Y para la cobertura de nubes
ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Cobertura de nubes (%)', color=color)
ax2.plot(filtered_df['date'], filtered_df['cloud_cover'], color=color, label='Cobertura de nubes')
ax2.tick_params(axis='y', labelcolor=color)

# Formatear el eje X para mostrar cada mes claramente
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gcf().autofmt_xdate() # Rotar las fechas para que se vean mejor

plt.title('Precipitaciones y Cobertura de Nubes (20/12/2021 - 08/09/2022)')
plt.show()
