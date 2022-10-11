from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

# chromedriver options
chrome_options = Options()
chrome_options.add_argument("--headless")

# chromedriver location
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://poe.ninja/challenge/skill-gems?level=16&quality=0-19&corrupted=No&gemType=Anomalous')
# accept cookies once
driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[3]/div[1]/button[2]').click()

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
gem_list = []
price_list = []

for gem in soup.findAll(attrs={'class': 'css-v20fs0'}):
    gem_index_to_string = str(gem)
    separate_gem_string = re.split('"|>|<', gem_index_to_string)
    gem_list.append(separate_gem_string[12])

for price in soup.findAll(attrs={'class': 'sorted sorted-desc css-aolo3q'}):
    price_index_to_string = str(price)
    separate_price_string = re.split('"|>|<', price_index_to_string)
    if separate_price_string[10] == 'Divine Orb':
        price_list.append(float(separate_price_string[16]) * 200)
    else:
        price_list.append(separate_price_string[16])

print(gem_list)
print(price_list)

