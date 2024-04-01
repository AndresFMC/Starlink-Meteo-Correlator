import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Cargar el DataFrame
hourly_dataframe = pd.read_csv('meteo_data.csv', parse_dates=['date'])

# Si las fechas ya son tz-aware y quieres asegurarte de que estén en UTC, puedes hacer esto:
# hourly_dataframe['date'] = hourly_dataframe['date'].dt.tz_convert('UTC')

# Filtrar el DataFrame para el rango de fechas deseado
start_date = pd.to_datetime("2021-12-20", utc=True)
end_date = pd.to_datetime("2022-09-08", utc=True)
mask = (hourly_dataframe['date'] >= start_date) & (hourly_dataframe['date'] <= end_date)
filtered_df = hourly_dataframe.loc[mask]

# Obtener la lista de todos los meses entre las fechas de inicio y fin
all_months = pd.date_range(start=start_date, end=end_date, freq='MS')

# Iterar sobre cada mes y crear una gráfica para ese mes
for single_date in all_months:
    month_start = single_date
    next_month_start = month_start + pd.offsets.MonthBegin(1)
    month_end = next_month_start - pd.Timedelta(days=1)
    
    # Filtrar el DataFrame para el mes actual
    mask = (filtered_df['date'] >= month_start) & (filtered_df['date'] <= month_end)
    monthly_df = filtered_df.loc[mask]
    
    if not monthly_df.empty:
        # Crear la figura y los ejes para el gráfico del mes actual
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:red'
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Precipitaciones (mm)', color=color)
        ax1.plot(monthly_df['date'], monthly_df['precipitation'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  
        color = 'tab:blue'
        ax2.set_ylabel('Cobertura de nubes (%)', color=color)
        ax2.plot(monthly_df['date'], monthly_df['cloud_cover'], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Formatear el eje X para mostrar días del mes
        ax1.xaxis.set_major_locator(mdates.DayLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

        plt.gcf().autofmt_xdate() # Rotar las fechas para que se vean mejor
        plt.title(f'Precipitaciones y Cobertura de Nubes ({month_start.strftime("%b %Y")})')
        plt.show()
