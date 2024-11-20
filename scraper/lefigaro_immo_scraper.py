from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
from bs4 import BeautifulSoup
from parse_offers import parse_html
import json
import yaml

#--------------------------------------------------------------#
#  Load configurations
#--------------------------------------------------------------#
with open("./config.yml", 'r') as file:
    try :
       config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)


BASE_URL = config["urls"]["BASE_URL"]
url = config["urls"]["url"]
BASE_PATH = config["paths"]["html_pages_directory"]
url_template = BASE_URL + url
scraped_data_path = config["paths"]["scraped_data_directory"]

#--------------------------------------------------------------#
#  functions to scrap, parse and save Data
#--------------------------------------------------------------#

def get_page_source(driver, url: str):
    """Récupérer la page source HTML.

    Args:
        driver (driver): driver Chrom qui sera utilisé pour simuler un navigateur
        url (str): l'url à scraper

    Returns:
        html: page source Html
    """
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content__link")))
    return driver.page_source

def retrieve_urls(driver, url : str) -> list[str]:
    """Récupérer les URLs des offres à partir de la page principale et les retourne sous forme d'une liste

    Args:
        driver (): L'objet WebDriver de Selenium utilisé pour naviguer.
        url (str): L'URL de la page principale à visiter.
    Returns:
        list[str]: Une liste contenant les URLs des offres, construite à partir des liens trouvés sur la page.
    """
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content__link")))
    soup = BeautifulSoup(driver.page_source, "lxml")
    return [BASE_URL + offer['href'] for offer in soup.find_all("a", class_="content__link") if 'href' in offer.attrs]


def get_offers_by_url(driver, urls : list, page_nb: int, mock = False):
    """
    Extraire les pages de chaque URL d'offre, avec gestion des erreurs pour passer à l'URL suivante en cas de problème.

    Args:
        driver: L'objet WebDriver de Selenium.
        urls (list): Une liste d'URLs à traiter.
        page_nb (int): Numéro de page à utiliser pour la sauvegarde.
        mock (bool): Indique si la fonction doit sauvegarder les pages (mock) ou parser les données.

    Returns:
        list: Liste des pages HTML (si `mock` est True).
        list: Liste des données parsées (si `mock` est False).
    """
    results = []
    count = 1

    for url in urls:
        print(f"Processing URL {url}...")
        try:
            driver.get(url)
            time.sleep(random.randint(3, 5)) 

            if mock:
                # Sauvegarder le contenu HTML brut
                html_content = driver.page_source
                results.append(html_content)
                save_html(html_content, count, page_nb)
                count += 1
            else:
                # Extraire et parser les données
                html_content = driver.page_source
                parsed_data = parse_html(html_content)
                results.append(parsed_data)

        except Exception as e:
            print(f"Error processing {url}: {e}")
    save_data(results, scraped_data_path)
    return results

def save_data(data, file_name: str):
    os.makedirs("./figaro_immo_data", exist_ok=True)
    try:
        with open(file_name, "w", encoding='utf-8') as f_out:
            json.dump(data, f_out, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données : {e}")

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

def get_all_pages(driver, count=1, i_begin =1 , mock = True):
    """Récupérer toutes les pages avec la pagination."""
    for page_nb in range(i_begin, count + 1):
        page_url = url_template.format(page_nb)
        print(f"Processing page {page_nb}...")
        
        urls = retrieve_urls(driver, page_url)
        
        get_offers_by_url(driver,urls,page_nb)
        
        time.sleep(random.randint(2, 5))
