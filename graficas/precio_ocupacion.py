# import plotly.express as px
# import pandas as pd

# # Leer el archivo Excel desde una hoja específica
# df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# # Crear el gráfico de dispersión
# fig = px.scatter(df, x='precio', y='ocupacion', color='tipo', hover_data=['check-in', 'pax'],
#                  title='Precio vs. Ocupación',
#                  labels={'precio': 'Precio', 'ocupacion': 'Ocupación (%)'})

# # Personalizar el diseño de la gráfica
# fig.update_layout(width=960, height=500)

# # Mostrar la gráfica
# fig.show()
import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Lista de días de antelación
dias_antelacion_lista = [1]

# Crear una figura vacía
fig = px.scatter(title='Precio vs. Ocupación por días de antelación', labels={'precio': 'Precio', 'y': 'Ocupación (%)'})

# Definir paletas de colores para 'pax' y 'tipo'
color_map_pax = px.colors.qualitative.Set1
color_map_tipo = px.colors.qualitative.T10

# Iterar sobre cada día de antelación
for i, dias_antelacion in enumerate(dias_antelacion_lista):
    # Obtener los valores únicos de 'pax' y 'tipo'
    unique_pax = df['pax'].unique()
    unique_tipo = df['tipo'].unique()
    
    # Crear el gráfico de dispersión para el día de antelación actual
    scatter = px.scatter(df, x='precio', y=dias_antelacion, color='pax', hover_data=['check-in', 'pax'],
                         labels={'precio': 'Precio', dias_antelacion: f'Ocupación (%) a {dias_antelacion} días de antelación'},
                         color_discrete_map={ 'pax': color_map_pax[i % len(color_map_pax)], 'tipo': color_map_tipo[i % len(color_map_tipo)]})
    # Agregar el gráfico al gráfico principal
    fig.add_traces(scatter.data)

# Personalizar el diseño de la gráfica
fig.update_layout(width=960, height=500)

# Mostrar la gráfica
fig.show()

