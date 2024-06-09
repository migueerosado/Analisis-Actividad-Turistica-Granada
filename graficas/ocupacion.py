import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Días de antelación
dias_anticipacion = [1, 6, 8, 13, 15, 20, 22, 27]

# Crear el gráfico de barras apiladas
fig = px.bar(df, x='tipo', y=dias_anticipacion, color='pax', barmode='stack',
             title='Ocupación por Tipo de Alojamiento y Número de Personas',
             labels={'tipo': 'Tipo de Alojamiento', 'value': 'Ocupación (%)'})

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar la gráfica
fig.show()
