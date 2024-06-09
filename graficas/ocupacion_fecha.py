import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Derretir el DataFrame para convertir los días de antelación en una columna
df_melted = df.melt(id_vars=['check-in', 'tipo', 'pax', 'precio'], 
                    var_name='dias_anticipacion', value_name='ocupacion')

# Convertir 'dias_anticipacion' a entero
df_melted['dias_anticipacion'] = df_melted['dias_anticipacion'].astype(int)

# Crear el gráfico de área apilada
fig = px.area(df_melted, x='check-in', y='ocupacion', color='tipo',
              title='Ocupación por Fecha y Tipo de Alojamiento',
              labels={'check-in': 'Fecha', 'ocupacion': 'Ocupación (%)'})

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar la
fig.show()