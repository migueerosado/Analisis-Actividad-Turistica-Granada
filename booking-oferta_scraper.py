import asyncio
from playwright.async_api import async_playwright
import time

async def save_html_from_booking(url, city):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Configurar la cabecera "Accept-Language" para acceder a la página en español
        await page.set_extra_http_headers({'Accept-Language': 'es'})
        
        # Navegar a la URL con la cabecera del idioma configurada
        await page.goto(url)
        
        # Hacer clic en la casilla de Casas y Apartamentos
        await page.click('text=Casas y apartamentos enteros')
        time.sleep(2)  
        
        # Guardar el HTML en un archivo de texto después de seleccionar Casas y Apartamentos
        content = await page.content()
        with open(f'parser/{city}_casas_y_apartamentos.txt', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"HTML de Casas y Apartamentos en {city} guardado exitosamente.")
        
        # Deseleccionar la casilla de Casas y Apartamentos
        await page.click('text=Casas y apartamentos enteros')
        time.sleep(2)  
        
        # Hacer clic en la casilla de Hoteles
        await page.click('text=Hoteles')
        time.sleep(2)  
        
        # Guardar el HTML en un archivo de texto después de seleccionar Hoteles
        content = await page.content()
        with open(f'parser/{city}_hoteles.txt', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"HTML de Hoteles en {city} guardado exitosamente.")
        
        await browser.close()

async def main():
    urls = [
        {
            'url': 'https://www.booking.com/searchresults.es.html?ss=Madrid&ssne=Madrid&ssne_untouched=Madrid&efdco=1&label=es-es-booking-desktop-onknyt5TBrS8m9RnGd*6fgS652829001115%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1005414%3Ali%3Adec%3Adm&aid=2311236&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-390625&dest_type=city&checkin=2024-07-02&checkout=2024-07-04&group_adults=2&no_rooms=1&group_children=0&flex_window=7',
            'city': 'Madrid'
        },
        {
            'url': 'https://www.booking.com/searchresults.es.html?ss=M%C3%A1laga&ssne=M%C3%A1laga&ssne_untouched=M%C3%A1laga&efdco=1&label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AuXqhbMGwAIB0gIkNjc0ZjhmZTUtOTAyNy00ZDIyLTg2MzctOTY0ZWZjYjljMmJj2AIF4AIB&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-390787&dest_type=city&checkin=2024-09-25&checkout=2024-09-27&group_adults=2&no_rooms=1&group_children=0&flex_window=7',
            'city': 'Malaga'
        },
        {
            'url': 'https://www.booking.com/searchresults.es.html?ss=Granada&ssne=Granada&ssne_untouched=Granada&efdco=1&label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AoDq9bIGwAIB0gIkNTFmZWE3NTQtOGU3YS00ZTVjLTlmYTYtYzU4N2NjNDVkOTNj2AIF4AIB&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-384328&dest_type=city&checkin=2024-07-31&checkout=2024-08-02&group_adults=2&no_rooms=1&group_children=0&flex_window=7',
            'city': 'Granada'
        }
    ]
    
    tasks = [save_html_from_booking(url_info['url'], url_info['city']) for url_info in urls]
    await asyncio.gather(*tasks)

# Ejecutar la función asincrónica
asyncio.run(main())

# https://www.granadahoy.com/granada/turisticos-comiendo-viviendas-Centro-Granada-residenciales_0_1858914345.html
# https://www.ine.es/jaxiT3/Datos.htm?t=2072#_tabs-grafico
# https://www.20minutos.es/noticia/5121801/0/tu-ciudad-esta-saturada-de-pisos-turisticos-consultalo-en-este-mapa-interactivo-del-ine/
# https://www.abc.es/espana/andalucia/malaga/malaga-provincia-andalucia-mayor-concentracion-pisos-turisticos-20240507122657-nts.html?ref=https%3A%2F%2Fwww.abc.es%2Fespana%2Fandalucia%2Fmalaga%2Fmalaga-provincia-andalucia-mayor-concentracion-pisos-turisticos-20240507122657-nts.html