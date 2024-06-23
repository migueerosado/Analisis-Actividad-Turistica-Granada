import pandas as pd

# # Leer datos del archivo Excel
# data = pd.read_excel("../resultados/all_booking.xlsx", sheet_name="graficas")

# # Guardar los datos en un archivo CSV
# data.to_csv("datos.csv", index=False)

# print(data)

# # Leer datos del archivo Excel
# data = pd.read_excel("../resultados/all_booking.xlsx", sheet_name="graficas_precio")

# # Guardar los datos en un archivo CSV
# data.to_csv("precios.csv", index=False)

# print(data)

# //----------------------------------------------------------------------------------------//

# Leer datos del archivo Excel para 
data = pd.read_excel("../resultados/all_booking.xlsx", sheet_name="graficas_apartamentos")

# Guardar los datos en un archivo CSV
data.to_csv("csv/datos_apartamentos_7.csv", index=False)

print(data)

# Leer datos del archivo Excel
data = pd.read_excel("../resultados/all_booking.xlsx", sheet_name="graficas_hoteles")

# Guardar los datos en un archivo CSV
data.to_csv("csv/datos_hoteles_7.csv", index=False)

print(data)

