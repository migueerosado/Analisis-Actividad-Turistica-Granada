import plotly.express as px
import pandas as pd

# Leer el archivo Excel desde una hoja específica
df = pd.read_excel('../resultados/all_booking.xlsx', sheet_name='graficas')

print(df)

# # Crear el gráfico de pastel
# fig = px.pie(df, names='tipo', title='Distribución de Tipos de Alojamiento')

# # Personalizar el diseño de la gráfica
# fig.update_layout(width=960, height=500)

# # Mostrar la gráfica
# fig.show()

            # function updateLegend(filteredData, margin, filters, yVariable) {
            #     // Obtener colores únicos utilizados en el gráfico
            #     const filteredColorDomain = filteredData.map((d, i) => i);
            #     colorScale.domain(filteredColorDomain);
            #     const uniqueColors = Array.from(new Set(filteredData.map(d => colorScale(d[yVariable]))));
            
            #     // Añadir la leyenda
            #     const legend = d3.select("#legend-container").append("svg")
            #         .attr("width", innerWidth + margin.left + margin.right)
            #         .attr("height", 50) // Altura ajustada para la leyenda
            #         .append("g")
            #         .attr("class", "legend")
            #         .attr("transform", `translate(${margin.left}, 20)`);
            
            #     // Añadir elementos de la leyenda para cada color único
            #     const legendItems = legend.selectAll(".legend-item")
            #         .data(uniqueColors)
            #         .enter().append("g")
            #         .attr("class", "legend-item")
            #         .attr("transform", (d, i) => `translate(0, ${i * 20})`);
            
            #     // Añadir rectángulos de color
            #     legendItems.append("rect")
            #         .attr("x", 0)
            #         .attr("width", 10)
            #         .attr("height", 10)
            #         .attr("fill", d => d);
            
            #     // Texto explicativo basado en el contenido de 'filteredData' y 'yVariable'
            #     const legendText = filteredData.map(d => {
            #         const filtersText = Object.keys(filters).map(filter => `${filter}: ${d[filter]}`).join("<br>");
            #         return `${yVariable} - ${filtersText}`;
            #     });
            
            #     // Añadir texto explicativo
            #     legendItems.append("text")
            #         .attr("x", 20) // Ajustar la posición horizontal del texto
            #         .attr("y", 10) // Ajustar la posición vertical del texto
            #         .html((d, i) => legendText[i]);
            
            
            #     // Ajustar la altura del contenedor de la leyenda
            #     const legendHeight = Math.max(uniqueColors.length * 20 + 40, 50); // 20px por elemento + 40px de espacio adicional, mínimo 50px
            #     d3.select("#legend-container")
            #         .style("height", legendHeight + "px");
            # }