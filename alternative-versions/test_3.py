from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import pandas as pd
import os
import re

PRICE_XPATH = '/html/body/div[3]/section/div/main/section/div/div/div[2]/div[1]/div[2]/div/div[2]/div/span'
LOW_CONFIDENCE_XPATH = '/html/body/div[3]/section/div/main/section/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div'
COOKIES_XPATH = '/html/body/div[7]/div/div/div[3]/div[1]/button[2]'
SHOW_ALL_XPATH = '/html/body/div[3]/section/div/main/section/div/div/div/button'

gem_name_list = []
list_of_base_gem_links = []
base_price_list = []
list_of_failed_gem_links = []
failed_price_list = []
list_of_successful_gem_links = []
successful_price_list = []
low_confidence_list = []

# chromedriver options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=640,360")

# chromedriver location
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

link = input('Please enter link to start testing: ')
driver.get(link)
sleep(0.5)
# accept cookies once
driver.find_element(By.XPATH, COOKIES_XPATH).click()

# keep clicking show all button until the whole page is shown
while True:
    try:
        driver.find_element(By.XPATH, SHOW_ALL_XPATH).click()
    except NoSuchElementException:
        break

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# scrape initial names and links
for g in soup.findAll('a', href=True, attrs={'class': 'css-v20fs0'}):
    g_str = str(g)
    gem_link = re.split('["<>]', g_str)
    # save gem names in list
    gem_name_list.append((gem_link[12]))
    # save links in list
    list_of_base_gem_links.append(gem_link[6])

# make alternative links for 20/20 gems
for link in list_of_base_gem_links:
    if link[-2:] == '20':
        list_of_failed_gem_links.append(link[:-4] + '20-20c')
    else:
        list_of_failed_gem_links.append(link[:-1] + '20-20c')

# make alternative links for 21/20 gems
for link in list_of_base_gem_links:
    if link[-2:] == '20':
        list_of_successful_gem_links.append(link[:-4] + '21-20c')
    else:
        list_of_successful_gem_links.append(link[:-1] + '21-20c')

# price checker dictionary
check = {
    '0k': '000',
    '1k': '100',
    '2k': '200',
    '3k': '300',
    '4k': '400',
    '5k': '500',
    '6k': '600',
    '7k': '700',
    '8k': '800',
    '9k': '900',
}


# checking the prices of all collected gems
def price_checker(gem_list, price_list):
    for gem in tqdm(gem_list):
        try:
            driver.get(f"https://poe.ninja{gem}")
            sleep(0.4)
            gem_price_value = driver.find_element(By.XPATH, PRICE_XPATH)
            gem_price_value_str = gem_price_value.text

            try:
                price_value = gem_price_value_str.split('.')[0] + check[gem_price_value_str.split('.')[1]]
            except KeyError:
                price_value = gem_price_value_str
            price_list.append(price_value)

            # check low confidence, only for 21/20 gems
            try:
                if gem_list == list_of_successful_gem_links:
                    driver.find_element(By.XPATH, LOW_CONFIDENCE_XPATH)
                    low_confidence_list.append('Yes')
            except NoSuchElementException:
                if gem_list == list_of_successful_gem_links:
                    low_confidence_list.append('No')

        except NoSuchElementException:
            # if no page is found add 0 for price and No for low confidence
            price_list.append(0)
            if gem_list == list_of_successful_gem_links:
                low_confidence_list.append('No')
            continue


price_checker(list_of_base_gem_links, base_price_list)
price_checker(list_of_failed_gem_links, failed_price_list)
price_checker(list_of_successful_gem_links, successful_price_list)

df = pd.DataFrame({'Gem Name': gem_name_list,
                   'Base': base_price_list,
                   '20/20': failed_price_list,
                   '21/20': successful_price_list,
                   'Low confidence': low_confidence_list})

if not os.path.isfile('../gems.csv'):
    df.to_csv('gems.csv', index=False, encoding='utf-8')
else:
    df.to_csv('gems.csv', mode='a', index=False, encoding='utf-8')
