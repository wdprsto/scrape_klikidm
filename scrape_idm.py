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
CSV_FILE_NAME = "test.csv"

# init subcategory
html = driver.page_source
beautifulSoupText = BeautifulSoup(html, "html.parser")

for sub_cat in beautifulSoupText.select('div[class*="section-kategori"]'):
    # try:
        subcat_data = sub_cat.select('div[class*="headline"]')[0].find('a')
        sub_cat_list[subcat_data.text] = subcat_data.get('href')
    # except: 
    #     continue

# print(sub_cat_list)
"""
INITIALISASI CSV PENAMPUNG
"""
with open(CSV_FILE_NAME, "a", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['prod_name','prod_cat','prod_link'])

"""
ITERASI UNTUK TIAP SUB KATEGOIR
"""

for sc_name, sc_link in sub_cat_list.items():
    data = []

    # buka linknya
    driver.get(sc_link)
    sub_html = driver.page_source

    sub_beautifulSoupText = BeautifulSoup(sub_html, "html.parser")

    # definisikan variabel penting
    MAX_PAGE = sub_beautifulSoupText.select_one('select[class*="pagelist"] option:last-child').text # max page of the subcategory..
    # selector can be modified to get specific element inside it. co: div:nth-of-type(2)
    
    for idx in range(1, int(MAX_PAGE)+1):
        if not idx == 1: 
            driver.get(f"{sc_link}?page={idx}")
            sub_html = driver.page_source

            sub_beautifulSoupText = BeautifulSoup(sub_html, "html.parser")

        items = sub_beautifulSoupText.select('div[class*="product-collection"] > div[class="item"]')
        
        for item in items:
            prod_link = item.select_one('a').get('href')
            prod_name = item.find('div', attrs={'class':'title'}).text.strip()
            data.append((prod_name, sc_name, prod_link))

    # write to csv
    with open(CSV_FILE_NAME, "a", newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # The for loop
        for prod_name, prod_cat, prod_link in data:
            writer.writerow([prod_name, prod_cat, prod_link])
