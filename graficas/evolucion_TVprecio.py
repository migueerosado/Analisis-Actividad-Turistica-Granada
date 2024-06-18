import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Leer datos desde el archivo Excel
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='TV_precio')
# df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='TV_PrecioHotel')

# Convertir la columna 'check-in' a tipo datetime
df['check-in'] = pd.to_datetime(df['check-in'])

# Filtrar solo las columnas necesarias y transponer el DataFrame
columns_to_plot = [1, 6, 8, 13, 15, 20, 22, 27]
df_filtered = df[['check-in'] + columns_to_plot]
df_transposed = df_filtered.set_index('check-in').T

# Configurar la figura
plt.figure(figsize=(12, 6))

# Obtener una paleta de colores amplia excluyendo el blanco
colors = [color for color in list(mcolors.TABLEAU_COLORS.keys()) + list(mcolors.BASE_COLORS.keys()) if color != 'w']

# Definir diferentes tipos de marcadores
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'd', '|', '_', 'X', 'D', 'O']

# Graficar la evolución de los valores con colores y marcadores únicos
for i, column in enumerate(df_transposed.columns):
    plt.plot(df_transposed.index, df_transposed[column], marker=markers[i % len(markers)], 
             color=colors[i % len(colors)], label=column.strftime('%Y-%m-%d'))

# Configurar etiquetas y título
plt.xlabel('Días de Antelación')
plt.ylabel('Variacion Precio (%)')
plt.title('Evolución de TV Precio a lo Largo de los días')

# Mover la leyenda fuera de la gráfica
plt.legend(title='Fechas de Check-in', loc='upper left', bbox_to_anchor=(1, 1))

plt.grid(True)

# Mostrar la gráfica
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

