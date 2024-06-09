import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Crear la gráfica
fig = px.area(df, x='check-in', y='pax', color='tipo', 
              title='Desempleo por Industria a lo largo del Tiempo')

# Personalizar el diseño de la gráfica
fig.update_layout(
    margin=dict(l=60, r=60, t=60, b=60), # Ajuste de márgenes
    yaxis=dict(showgrid=True),           # Mostrar la cuadrícula en el eje Y
    legend=dict(orientation="h", x=0.5, xanchor="center", y=1.1), # Configuración de la leyenda
)

# Mostrar la gráfica
fig.show()
