import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Crear el gráfico de caja
fig = px.violin(df, x='tipo', y='precio',  box=True,
             title='Distribución de Precios por Tipo de Alojamiento',
             labels={'tipo': 'Tipo de Alojamiento', 'precio': 'Precio ($)'})

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar la gráfica
fig.show()
