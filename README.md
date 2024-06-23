# Análisis de la Actividad Turística en Granada

Este proyecto analiza la actividad turística en Granada mediante la recopilación automática de datos de diferentes plataformas turísticas. Se presenta una herramienta web interactiva que muestra la dinámica turística de la ciudad.

## Requisitos Previos

- Python 3.7 o superior
- Dependencias de Python listadas en `requirements.txt`

## Instalación

1. **Clona el repositorio:**
    ```sh
    git clone https://github.com/migueerosado/Analisis-Actividad-Turistica-Granada.git
    cd Analisis-Actividad-Turistica-Granada
    ```

2. **Crea un entorno virtual e instala las dependencias:**
    ```sh
    python -m venv venv
    source venv/bin/activate # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Ejecución de los Scripts de Scraping

Los scripts de scraping recolectan datos de Booking.com sobre la disponibilidad de alojamientos y la oferta turística en Granada.

### Script de Scraping de Disponibilidad de Alojamientos

1. **Ubicación del script:**
    - `booking_scraper.py`

2. **Ejecución del script:**
    ```sh
    python booking_scraper.py
    ```

### Script de Scraping de Oferta Turística

1. **Ubicación del script:**
    - `booking-oferta_scraper.py`

2. **Ejecución del script:**
    ```sh
    python booking-oferta_scraper.py
    ```

### Ejemplo de Uso del Script de Scraping de Disponibilidad de Alojamientos

```python
from playwright.sync_api import sync_playwright

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.booking.com')
        # Añade aquí tu código de scraping
        browser.close()

if __name__ == "__main__":
    run_scraper()
```

## Ejecución de la Aplicación Web

Para ejecutar la aplicación web localmente, sigue estos pasos:

1. **Navega al directorio del proyecto:**
    ```sh
    cd web
    ```

2. **Inicia el servidor HTTP:**
    ```sh
    python -m http.server
    ```

3. **Abre un navegador web y accede a:**
    ```
    http://localhost:8000/rutadelarchivo
    ```

## Estructura del Proyecto

- `booking_scraper.py`: Script para scraping de disponibilidad de alojamientos en Booking.com.
- `booking-oferta_scraper.py`: Script para scraping de oferta turística en Booking.com.
- `web/`: Directorio que contiene los archivos de la aplicación web.
- `resultados/`: Directorio donde se almacenan los datos recopilados de booking_scraper.py.
- `parser/`: Directorio donde se almacenan los datos recopilados de booking-oferta_scraper.py
- `graficas/`: Directorio donde se almacenan las gráficos de los distintos datos recopilados.
- `requirements.txt`: Archivo con las dependencias de Python necesarias.


