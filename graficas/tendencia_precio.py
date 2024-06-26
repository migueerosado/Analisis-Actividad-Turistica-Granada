import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas_apartamentos')

# Convertir la columna 'check-in' a tipo datetime para utilizarla como eje x
df['check-in'] = pd.to_datetime(df['check-in'])

# Crear una nueva columna combinando tipo y pax
df['color'] = df['tipo'] + ' - ' + df['pax'].astype(str)

# Crear el gráfico de línea de tendencia para ambos tipos de alojamiento
fig = px.line(df, x='check-in', y='precio', color='color',
              title='Tendencia de Precios de Apartamentos y Hoteles a lo Largo del Tiempo',
              labels={'check-in': 'Fecha', 'precio': 'Precio ($)', 'pax': 'Número de Personas',
                      'tipo': 'Tipo de Alojamiento', 'color': 'Color (Tipo - Pax)'})

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar el gráfico
fig.show()

