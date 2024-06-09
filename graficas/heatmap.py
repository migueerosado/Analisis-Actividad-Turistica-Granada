import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Días de antelación
dias_anticipacion = [1, 6, 8, 13, 15, 20, 22, 27]

# Crear el mapa de calor
fig = px.imshow(df[dias_anticipacion].T, x=df['tipo'], y=dias_anticipacion,
                labels={'x': 'Tipo de Alojamiento', 'y': 'Días de Antelación', 'color': 'Ocupación (%)'},
                title='Mapa de Calor de Ocupación por Fecha y Tipo de Alojamiento')

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar la gráfica
fig.show()
