import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Días de antelación
dias_anticipacion = [1]

df = df[df['tipo'] == "Apartamentos"]
# df = df[df['tipo'] == "Hotel"]

# Convertir la columna 'check-in' a tipo datetime para utilizarla como eje x
df['check-in'] = pd.to_datetime(df['check-in'])

# Crear el gráfico de línea de tendencia
fig = px.line(df, x='check-in', y=dias_anticipacion, color= 'pax',
              title='Tendencia de Ocupación a lo Largo del Tiempo',
              labels={'check-in': 'Fecha', 'value': 'Ocupación (%)'})

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar la gráfica
fig.show()



