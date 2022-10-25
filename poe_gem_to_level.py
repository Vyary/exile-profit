import os
import re
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

PRICE_XPATH = '/html/body/div[3]/section/div/main/section/div/div/div[2]/div[1]/div[2]/div/div[2]/div/span'
LOW_CONFIDENCE_XPATH = '/html/body/div[3]/section/div/main/section/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div'
COOKIES_XPATH = '/html/body/div[7]/div/div/div[3]/div[1]/button[2]'
SHOW_ALL_XPATH = '/html/body/div[3]/section/div/main/section/div/div/div/button'
NORMAL_LINK = 'https://poe.ninja/challenge/skill-gems?level=1&quality=20&corrupted=No&gemType=Normal'
ANOMALOUS_LINK = 'https://poe.ninja/challenge/skill-gems?level=16&quality=0-19&corrupted=No&gemType=Anomalous'
DIVERGENT_LINK = 'https://poe.ninja/challenge/skill-gems?level=16&quality=0-19&corrupted=No&gemType=Divergent'
PHANTASMAL_LINK = 'https://poe.ninja/challenge/skill-gems?level=16&quality=0-19&corrupted=No&gemType=Phantasmal'

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


def initiate_driver(link):
    # chromedriver location
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)
    driver.implicitly_wait(1)
    driver.get(link)
    # accept cookies once
    driver.find_element(By.XPATH, COOKIES_XPATH).click()

    # keep clicking on show all button until the whole page is shown
    while True:
        try:
            driver.find_element(By.XPATH, SHOW_ALL_XPATH).click()
        except NoSuchElementException:
            break

    content = driver.page_source
    return content


def initial_page_scrape(content):
    soup = BeautifulSoup(content, 'html.parser')
    for g in soup.findAll('a', href=True, attrs={'class': 'css-v20fs0'}):
        gem_link = re.split('["<>]', str(g))
        # save gem names in list
        gem_name_list.append((gem_link[12]))
        # save links in list
        list_of_base_gem_links.append(gem_link[6])


# function to make lists with alternative urls for 20-20 and 21-20 gems
def alternative_link_maker(gem_list, gem_type):
    for link in list_of_base_gem_links:
        if link[-2:] == '20':
            gem_list.append(link[:-4] + gem_type)
        else:
            gem_list.append(link[:-1] + gem_type)


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


# converting price from decimal separated to a whole number. example: from 1.3k to 1300
def price_converter(value):
    try:
        price_value = value.split('.')[0] + check[value.split('.')[1]]
    except KeyError:
        price_value = value
    return price_value


def low_confidence(driver):
    try:
        driver.find_element(By.XPATH, LOW_CONFIDENCE_XPATH)
        return 'Yes'
    except NoSuchElementException:
        return 'No'


def price_checker(gem_list, price_list):
    # chromedriver location
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)
    driver.implicitly_wait(1)
    for gem in tqdm(gem_list):
        try:
            driver.get(f"https://poe.ninja{gem}")
            gem_price_value = driver.find_element(By.XPATH, PRICE_XPATH)
            gem_price_value_str = gem_price_value.text
            # convert price example: 1.3k to 1300
            price_list.append(price_converter(gem_price_value_str))
            # check confidence of 21/20 gems
            if gem_list == list_of_successful_gem_links:
                low_confidence_list.append(low_confidence(driver))
        except NoSuchElementException:
            # if page is not found: add 0 for price and No for confidence
            price_list.append(0)
            if gem_list == list_of_successful_gem_links:
                low_confidence_list.append('No')


def save_data():
    df = pd.DataFrame({'Gem Name': gem_name_list,
                       'Base': base_price_list,
                       '20/20': failed_price_list,
                       '21/20': successful_price_list,
                       'Low confidence': low_confidence_list})

    if not os.path.isfile('gems.csv'):
        df.to_csv('gems.csv', index=False, encoding='utf-8')
    else:
        df.to_csv('gems.csv', mode='a', index=False, encoding='utf-8')


def main(test_link):
    initial_page_scrape(initiate_driver(test_link))
    alternative_link_maker(list_of_failed_gem_links, '20-20c')
    alternative_link_maker(list_of_successful_gem_links, '21-20c')
    price_checker(list_of_base_gem_links, base_price_list)
    price_checker(list_of_failed_gem_links, failed_price_list)
    price_checker(list_of_successful_gem_links, successful_price_list)
    save_data()


if __name__ == '__main__':
    testing_links = [NORMAL_LINK, ANOMALOUS_LINK, DIVERGENT_LINK, PHANTASMAL_LINK]
    with multiprocessing.Pool(4) as pool:
        pool.map(main, testing_links)
