from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://immobilier.lefigaro.fr"
url_template = BASE_URL + "/annonces/immobilier-location-maison-rhone+alpes.html?types=maison%2Bneuve,atelier,chalet,chambre%2Bd%2Bhote,manoir,moulin,propriete,ferme,gite,villa,appartement,loft,chambre,duplex&page={}"
BASE_PATH = "./BeautifulSoup/lefigaro_immo_scraping/alpes_Rhône"


def get_page_source(driver, url: str):
    """Récupérer la page source HTML."""
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content__link")))
    return driver.page_source

def retrieve_urls(driver, url):
    """Récupérer les URLs des offres."""
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content__link")))
    soup = BeautifulSoup(driver.page_source, "lxml")
    return [BASE_URL + offer['href'] for offer in soup.find_all("a", class_="content__link") if 'href' in offer.attrs]


def get_offers_by_url(driver, urls, page_nb):
    """Extraire les pages de chaque URL d'offre, avec gestion des erreurs pour passer à l'URL suivante en cas de problème."""
    pages = []
    count = 1
    for url in urls:
        print(f"Processing URL {url}...")
        try:
            driver.get(url)  
            time.sleep(random.randint(3, 5))  
            pages.append(driver.page_source)
            save_html(driver.page_source, count, page_nb)  
            count += 1
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue  
    
    return pages

def save_html(page,offer_nb : int, page_nb : int):
    """ save de hmtl page in directory (temporary)

    Args:
        page (_type_): _description_
        offer_nb (int): le numéro de l'offre scrapée pour construire le nom du fichier de sortie
        page_nb (int): le nombre de page scrapée pour contsruire le nom du fichier de sortie
    """
    os.makedirs(BASE_PATH, exist_ok=True)
    with open(BASE_PATH + f"/announce_{page_nb}_{offer_nb}.html","wb" ) as f_out:
        f_out.write(page.encode("utf-8"))

def get_all_pages(driver, count=1):
    """Récupérer toutes les pages avec la pagination."""
    for page_nb in range(1, count + 1):
        page_url = url_template.format(page_nb)
        print(f"Processing page {page_nb}...")
        
        urls = retrieve_urls(driver, page_url)
        
        get_offers_by_url(driver,urls,page_nb)
        
        time.sleep(random.randint(2, 5))


def main():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    with webdriver.Chrome(options=options) as driver:
        get_all_pages(driver, count = 22)

if __name__ == "__main__":
    main()
