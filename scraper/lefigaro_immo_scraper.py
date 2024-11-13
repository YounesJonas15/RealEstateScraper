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

