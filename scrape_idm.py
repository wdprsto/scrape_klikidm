# Necessary libraries are imported
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import csv

# Selenium webdriver is started and the login process is performed on Twitter
executable_path = "C:\\Users\\WahyuDP\\Documents\\_GitHub\\scrape-donut\\scrape-klikidm\\chromedriver_win32\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument(
    "user-data-dir=C:\\Users\\WahyuDP\\Documents\\_GitHub\\scrape-donut\\scrape-klikidm\\data")
options.add_argument("--start-maximized")
options.add_argument('--no-default-browser-check')
options.add_argument('--no-sandbox')
# options.add_argument('--headless') #biar jalan dibackground, prev:disabled
options.add_argument('--disable-gpu')
options.set_capability('unhandledPromptBehavior', 'dismiss')
options.add_experimental_option("detach", True)

# Instansiate webdriver
driver = webdriver.Chrome(executable_path=executable_path, options=options)
wait = WebDriverWait(driver, 10)

driver.get(f"https://www.klikindomaret.com/category/makanan")

"""
LIST SEMUA SUBKATEGORI
"""
# init variabel
sub_cat_list = {}

# init subcategory
html = driver.page_source
beautifulSoupText = BeautifulSoup(html, "html.parser")

for sub_cat in beautifulSoupText.select('div[class*="section-kategori"]'):
    # try:
        subcat_data = sub_cat.select('div[class*="headline"]')[0].find('a')
        sub_cat_list[subcat_data.text] = subcat_data.get('href')
    # except: 
    #     continue

print(sub_cat_list)

"""
ITERASI UNTUK TIAP SUB KATEGOIR
"""

for sc_name, sc_link in sub_cat_list.items():
    # buka linknya
    driver.get(sc_link)


    break; 