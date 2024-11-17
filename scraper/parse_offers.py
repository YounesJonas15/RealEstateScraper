import json
from bs4 import BeautifulSoup
import os

BASE_PATH = "./BeautifulSoup/lefigaro_immo_scraping/pays_de_la_loire"

def parse_atouts(soup):
    try:
        atouts_elements = soup.select("ul.asset-list li.asset-list--item")
        atouts = [element.get_text(strip=True) for element in atouts_elements]
    except Exception as e:
        print(f"Erreur lors de l'analyse des atouts : {e}")
        atouts = []
    return atouts

def parse_features(soup):
    try:
        features_elements = soup.find("ul", class_="features-list").find_all("li")
        features = []
        for item in features_elements:
            feature = item.find("span", class_="feature")
            if feature:
                features.append(feature.get_text(strip=True))
    except AttributeError:
        print("Aucune liste de fonctionnalités trouvée.")
        features = []
    except Exception as e:
        print(f"Erreur lors de l'analyse des fonctionnalités : {e}")
        features = []
    return features

def parse_html(page):
    try:
        soup = BeautifulSoup(page, "lxml")
        title = soup.find("div", class_="classified-main-infos-title")
        title = title.get_text(strip=True) if title else "null"

        price = soup.find("div", class_="classified-price-per-m2")
        price = price.get_text(strip=True) if price else "null"

        fees = soup.find("span", class_="fees")
        fees = fees.get_text(strip=True) if fees else "null"

        loyer_element = soup.find('span', class_='key__title', string='Loyer du bien par rapport à Paris 4ème')
        loyer_value = loyer_element.find_next('a').text if loyer_element else "Non trouvé"

        charges_element = soup.find('span', class_='key__title', string='Charges locatives')
        charges_value = charges_element.find_next('a').text if charges_element else "Non trouvé"

        honoraires_element = soup.find('span', class_='key__title', string='Honoraires')
        honoraires_value = honoraires_element.find_next('a').text if honoraires_element else "Non trouvé"

        bilan_energie_element = soup.find('span', class_='key__title', string='Bilan énergie du bien')
        bilan_energie_value = bilan_energie_element.find_next('span', class_='dpe-card').text if bilan_energie_element else "Non trouvé"

        score_eco_zone_element = soup.find('span', class_='key__title', string='Score Eco-Zone')
        score_eco_zone_value = score_eco_zone_element.find_next('a').text if score_eco_zone_element else "Non trouvé"

        atouts = parse_atouts(soup)
        features = parse_features(soup)
        
        data = {
            "title": title,
            "price": price,
            "fees": fees,
            "loyer": loyer_value,
            "charges": charges_value,
            "honoraires": honoraires_value,
            "bilan_energie": bilan_energie_value,
            "score_eco_zone_value": score_eco_zone_value,
            "atouts": atouts,
            "features": features
        }
    except Exception as e:
        print(f"Erreur lors de l'analyse HTML : {e}")
        data = {}
    return data

def parse_pages():
    results = []
    pages_path = os.listdir(BASE_PATH)

    for page_path in pages_path:
        try:
            with open(os.path.join(BASE_PATH, page_path), 'r', encoding="utf-8") as file:
                page = file.read()
            print("processing : ", page_path)
            result = parse_html(page)
            results.append(result)
        except FileNotFoundError:
            print(f"Le fichier {page_path} est introuvable.")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier {page_path} : {e}")
    return results

def save_data(data, file_name: str):
    os.makedirs("./figaro_immo_data", exist_ok=True)
    try:
        with open(file_name, "w", encoding='utf-8') as f_out:
            json.dump(data, f_out, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données : {e}")

def main():
    print("Répertoire actuel :", os.getcwd())
    data = parse_pages()
    save_data(data, "./scraped_data/pays_de_la_loire_data.json")

if __name__ == '__main__':
    main()
