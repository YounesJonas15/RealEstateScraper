from lefigaro_immo_scraper import get_all_pages
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def main():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    with webdriver.Chrome(options=options) as driver:
        get_all_pages(driver, count = 1)

if __name__ == "__main__":
    main()