import { promisify } from "util";
import * as d3 from "d3";

// Cargar los datos desde el archivo Excel
const readXlsx = promisify(require("xlsx").readFile);
const workbook = await readXlsx("resultados/all_booking.xlsx");
const sheetName = "metodos";
const data = d3.csvParse(d3.csvFormatRows(workbook.Sheets[sheetName]));

// Especificar las dimensiones del gráfico.
const width = 928;
const height = 500;
const marginTop = 10;
const marginRight = 10;
const marginBottom = 20;
const marginLeft = 60; // Ajustado para que coincida con el original.

// Determinar las series que necesitan ser apiladas.
const series = d3.stack()
  .offset(d3.stackOffsetWiggle)
  .order(d3.stackOrderInsideOut)
  .keys(d3.union(data.map(d => d.industry))) // Claves de series distintas, en orden de entrada.
  .value(([, D], key) => D.get(key).unemployed) // Obtener el valor para cada clave de serie y apilar.
  (d3.index(data, d => d.date, d => d.industry)); // Agrupar por apilamiento y luego por clave de serie.

// Preparar las escalas para codificaciones de posición y color.
const x = d3.scaleUtc()
  .domain(d3.extent(data, d => d.date))
  .range([marginLeft, width - marginRight]);

const y = d3.scaleLinear()
  .domain(d3.extent(series.flat(2)))
  .rangeRound([height - marginBottom, marginTop]);

const color = d3.scaleOrdinal()
  .domain(series.map(d => d.key))
  .range(d3.schemeTableau10);

// Construir una forma de área.
const area = d3.area()
  .x(d => x(d.data[0]))
  .y0(d => y(d[0]))
  .y1(d => y(d[1]));

// Crear el contenedor SVG.
const svg = d3.create("svg")
  .attr("viewBox", [0, 0, width, height])
  .attr("width", width)
  .attr("height", height)
  .attr("style", "max-width: 100%; height: auto;");

// Agregar el eje y, eliminar la línea de dominio, agregar líneas de cuadrícula y una etiqueta.
svg.append("g")
  .attr("transform", `translate(${marginLeft},0)`)
  .call(d3.axisLeft(y).ticks(height / 80).tickFormat((d) => Math.abs(d).toLocaleString("en-US")))
  .call(g => g.select(".domain").remove())
  .call(g => g.selectAll(".tick line").clone()
    .attr("x2", width - marginLeft - marginRight)
    .attr("stroke-opacity", 0.1))
  .call(g => g.append("text")
    .attr("x", -marginLeft)
    .attr("y", 10)
    .attr("fill", "currentColor")
    .attr("text-anchor", "start")
    .text("↑ Unemployed persons"));

// Añadir el eje x y eliminar la línea de dominio.
svg.append("g")
  .attr("transform", `translate(0,${height - marginBottom})`)
  .call(d3.axisBottom(x).tickSizeOuter(0))
  .call(g => g.select(".domain").remove());

// Añadir una ruta para cada serie.
svg.append("g")
  .selectAll()
  .data(series)
  .join("path")
  .attr("fill", d => color(d.key))
  .attr("d", area)
  .append("title")
  .text(d => d.key);

// Retornar el gráfico con la escala de colores como propiedad (para la leyenda).
const chart = Object.assign(svg.node(), { scales: { color } });

// Visualizar el gráfico.
chart;
