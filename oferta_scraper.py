import requests
import asyncio
from playwright.async_api import async_playwright
import time

async def save_html_from_booking():
   
    url = 'https://www.booking.com/searchresults.es.html?ss=Granada&ssne=Granada&ssne_untouched=Granada&efdco=1&label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AoDq9bIGwAIB0gIkNTFmZWE3NTQtOGU3YS00ZTVjLTlmYTYtYzU4N2NjNDVkOTNj2AIF4AIB&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-384328&dest_type=city&checkin=2024-07-31&checkout=2024-08-02&group_adults=2&no_rooms=1&group_children=0&flex_window=7'

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
        with open('parser/casas_y_apartamentos.txt', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("HTML de Casas y Apartamentos guardado exitosamente.")
        
        # Deseleccionar la casilla de Casas y Apartamentos
        await page.click('text=Casas y apartamentos enteros')
        time.sleep(2)  
        
        # Hacer clic en la casilla de Hoteles
        await page.click('text=Hoteles')
        time.sleep(2)  
        
        # Guardar el HTML en un archivo de texto después de seleccionar Hoteles
        content = await page.content()
        with open('parser/hoteles.txt', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("HTML de Hoteles guardado exitosamente.")
        
        await browser.close()

# Ejecutar la función asincrónica
asyncio.run(save_html_from_booking())
