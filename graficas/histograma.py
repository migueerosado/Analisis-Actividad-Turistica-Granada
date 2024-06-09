import plotly.graph_objects as go
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

# Días de antelación
dias_anticipacion = [1, 6, 8, 13, 15, 20, 22, 27]

# Colores para cada número de personas (pax)
colores = {2: 'blue', 4: 'green', 5: 'orange', 7: 'red'}

# Crear una figura de Plotly
fig = go.Figure()

# Agregar líneas para cada tipo de alojamiento
for tipo in df['tipo'].unique():
    df_tipo = df[df['tipo'] == tipo]
    for pax in df_tipo['pax'].unique():
        df_pax = df_tipo[df_tipo['pax'] == pax]
        ocupacion_media = df_pax[dias_anticipacion].mean()
        # Asignar estilo visual para cada tipo de alojamiento
        if tipo == 'Apartamentos':
            line_dash = 'solid'
        else:
            line_dash = 'dash'
        fig.add_trace(go.Scatter(
            x=dias_anticipacion, y=ocupacion_media,
            mode='lines+markers',
            name=f"{tipo} ({pax} pax)",
            line=dict(shape='linear', dash=line_dash),
            marker=dict(color=colores[pax])
        ))

# Personalizar el diseño de la gráfica
fig.update_layout(
    title='Ocupación en función de los días de antelación',
    xaxis_title='Días de antelación',
    yaxis_title='Ocupación (%)',
    width=960,
    height=500,
    xaxis=dict(tickmode='linear')
)

# Mostrar la gráfica
fig.show()
