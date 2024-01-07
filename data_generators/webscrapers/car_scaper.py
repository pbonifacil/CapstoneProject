from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from StringProgressBar import progressBar
import pickle
import pandas as pd
import time


def scrap_car_specs(links_to_listings):
    geckodriver_path = r'selenium/geckodriver.exe'
    dr = webdriver.Firefox(
        service=webdriver.firefox.service.Service(executable_path=geckodriver_path))  # initialize firefox web driver
    dataset = []
    for link in links_to_listings:
        dr.get(link)
        try:
            price_comparison = WebDriverWait(dr, 4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "p.esicnpr2"))).text  # Price comparison is dynamic content and takes some time to let it load before extracting the element
        except Exception as e:
            price_comparison = "Não disponível"

        soup = BeautifulSoup(dr.page_source, "html.parser")

        specs_html = soup.find_all("div", class_="ooa-13nyoul e1iqsx44")
        specs = {list(pair.children)[0].text: list(pair.children)[1].text for pair in specs_html}

        try:
            specs['Foto'] = soup.find("img", class_="ooa-jcur4u e1ejyjdh16").get("src")
        except Exception as e:
            specs['Foto'] = "Não disponível"
        if not soup.find("h3", class_="offer-price__number esicnpr5 ooa-17vk29r er34gjf0"):
            continue
        specs['Preço'] = soup.find("h3", class_="offer-price__number esicnpr5 ooa-17vk29r er34gjf0").text
        specs['Link'] = link
        specs['PreçoComparado'] = price_comparison
        try:
            specs['Morada'] = soup.find_all("a", class_="eavtgmy0 ooa-1j0jeo9")[2].text
        except Exception as e:
            specs['Morada'] = 'Não disponível'
        specs['Acessórios'] = [accessory.text for accessory in
                               soup.find_all("p", class_="evccnj10 ooa-1i4y99d er34gjf0")]

        dataset.append(specs)
        # PROGRESS BAR
        progress_bar = progressBar.filledBar(len(links_to_listings), len(dataset))
        print(progress_bar[0] + " - " + str(round(progress_bar[1], 2)) + f"%  -  {len(dataset)} cars scraped...",
              end="\r")
        time.sleep(2)
    dr.close()
    return dataset


if __name__ == "__main__":
    with open("listing_links.pkl", "rb") as fa:
        links = pickle.load(fa)

    batch_size = 500
    for i in range(0, len(links), batch_size):
        batch_links = links[i:i + batch_size]
        data = scrap_car_specs(batch_links)
        df = pd.DataFrame(data)
        csv_filename = f"car_dataset_{i}_{i + batch_size}.csv"
        df = df[['Anunciante', 'Marca', 'Modelo', 'Versão', 'Combustível', 'Ano',
                 'Quilómetros', 'Cilindrada', 'Potência', 'Segmento', 'Cor',
                 'Tipo de Caixa', 'Nº de portas', 'Garantia de Stand (incl. no preço)',
                 'Condição', 'Foto', 'Preço', 'Link', 'PreçoComparado', 'Morada', 'Consumo Urbano']]
        df.to_csv(csv_filename, encoding='utf-8-sig')
        print(f"Saved {csv_filename}")