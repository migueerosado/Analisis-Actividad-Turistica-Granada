import re
from playwright.sync_api import sync_playwright
from textblob import TextBlob
import pandas as pd
import time
import datetime


def scrape_capacity(page):
    capacity_text = page.locator('//div[@data-testid="notices-container"]').inner_text()
    capacity_number = None
    if capacity_text:
        # Buscar un número dentro del texto
        match = re.search(r'\d+', capacity_text)
        if match:
            capacity_number = int(match.group())  # Convertir el texto coincidente en un número entero
    return capacity_number

def scrape_results(page, accommodation_type, checkin, checkout, num_adults, num_children):
    capacity = scrape_capacity(page)
    accommodations = page.locator('//div[@data-testid="property-card"]').all()
    results = []

    for accommodation in accommodations:
        accommodation_dict = {}
        accommodation_dict['type'] = accommodation_type
        accommodation_dict['capacity'] = capacity
        accommodation_dict['check-in'] = checkin
        accommodation_dict['check-out'] = checkout
        accommodation_dict['num_adults'] = num_adults
        accommodation_dict['num_children'] = num_children

        try:
            accommodation_dict['name'] = accommodation.locator('//div[@data-testid="title"]').inner_text(timeout=5000)
        except Exception as e:
            print(f"Error al obtener el nombre del {accommodation_type.lower()}: {e}")
            accommodation_dict['name'] = "-"

        try:
            accommodation_dict['price'] = accommodation.locator('//span[@data-testid="price-and-discounted-price"]').inner_text(timeout=5000)
        except Exception as e:
            print(f"Error al obtener el precio del {accommodation_type.lower()}: {e}")
            accommodation_dict['price'] = "-"

        try:
            accommodation_dict['score'] = accommodation.locator('//div[@data-testid="review-score"]/div[1]').inner_text(timeout=5000)
        except Exception as e:
            print(f"Error al obtener la puntuación del {accommodation_type.lower()}: {e}")
            accommodation_dict['score'] = "-"

        try:
            accommodation_dict['avg_review'] = accommodation.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text(timeout=5000)
        except Exception as e:
            print(f"Error al obtener la revisión promedio del {accommodation_type.lower()}: {e}")
            accommodation_dict['avg_review'] = "-"

        try:
            reviews_count = accommodation.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text(timeout=5000)
            accommodation_dict['reviews_count'] = reviews_count.split()[0] if reviews_count else "-"
        except Exception as e:
            print(f"Error al obtener el conteo de revisiones del {accommodation_type.lower()}: {e}")
            accommodation_dict['reviews_count'] = "-"

        results.append(accommodation_dict)

    return results

def main():
    with sync_playwright() as p:
        checkin_date = ['2024-06-06', '2024-06-11', '2024-06-13', '2024-06-18', '2024-06-20', '2024-06-25', '2024-06-27', '2024-07-02']
        checkout_date = ['2024-06-09', '2024-06-14', '2024-06-16', '2024-06-21', '2024-06-23', '2024-06-28', '2024-06-30', '2024-07-04']
        num_adults = ['2', '2', '5', '4' , '7']
        num_children = ['0', '2', '0', '3', '0']
        all_results = []

        for checkin, checkout in zip(checkin_date, checkout_date):
            for adults, children in zip(num_adults, num_children):
                page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin}&checkout={checkout}&selected_currency=USD&ss=Granada&ssne=Granada&ssne_untouched=Granada&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults={adults}&no_rooms=1&group_children={children}&sb_travel_purpose=leisure'

                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
                page.goto(page_url)

                time.sleep(1) 
   
                # Búsqueda de apartamentos
                page.click('text=Apartments')
                time.sleep(2)  # Pausa para que la página se cargue completamente
                apartment_results = scrape_results(page, "Apartamentos", checkin, checkout, adults, children)
                all_results.extend(apartment_results)

                page.click('text=Apartments')

                time.sleep(2)
                # Búsqueda de hoteles
                page.click('text=Hotels')
                time.sleep(2)  # Pausa para que la página se cargue completamente
                hotel_results = scrape_results(page, "Hotel", checkin, checkout, adults, children)
                all_results.extend(hotel_results)
                
                browser.close()

        
        # Crear DataFrame con todos los resultados
        df = pd.DataFrame(all_results)
        
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

        # Agregar la columna de fecha actual al DataFrame
        df['Fecha'] = None
        df.at[0, 'Fecha'] = fecha_actual

        # Guardar en Excel
        df.to_excel('resultados/lista_booking22.xlsx', index=False)

        # Guardar en CSV
        df.to_csv('resultados/lista_booking22.csv', index=False)

if __name__ == '__main__':
    main()

