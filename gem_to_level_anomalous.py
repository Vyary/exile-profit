from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import pandas as pd

list_of_links = []
gem_name_list = []
base_gems_price_list = []
failed_gems_price_list = []
successful_gems_price_list = []

base_gems_link = 'https://poe.ninja/challenge/skill-gems?level=16&quality=0-19&corrupted=No&gemType=Anomalous'
failed_gems_link = 'https://poe.ninja/challenge/skill-gems?level=20&quality=20&corrupted=Yes&gemType=Anomalous'
successful_gems_link = 'https://poe.ninja/challenge/skill-gems?level=21&quality=20&corrupted=Yes&gemType=Anomalous'

name_xpath = '/html/body/div[3]/section/div/main/section/div/div/div[1]/div/div/h1'
price_xpath = '/html/body/div[3]/section/div/main/section/div/div/div[2]/div[1]/div[2]/div/div[2]/div/span'

# chromedriver options
chrome_options = Options()
chrome_options.add_argument("--headless")


def initial_names_and_price(base_link):
    # chromedriver location
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_link)
    # accept cookies once
    driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[3]/div[1]/button[2]').click()

    sleep(1)
    # sort by name
    driver.find_element(By.XPATH, '/html/body/div[3]/section/div/main/section/div/div/div/div[3]/div/table/thead/tr/'
                                  'th[1]').click()
    sleep(0.5)
    driver.find_element(By.XPATH, '/html/body/div[3]/section/div/main/section/div/div/div/div[3]/div/table/thead/tr/'
                                  'th[1]').click()

    # show all
    while True:
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/section/div/main/section/div/div/div/button').click()
        except NoSuchElementException:
            break

    # scrape page
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    for g in soup.findAll('a', href=True, attrs={'class': 'css-v20fs0'}):
        g_str = str(g)
        gem_link = g_str.replace('<a aria-label="See more details about undefined" class="css-v20fs0" href="', '') \
            .replace('</span></a>', '').split('"><span class="css-106k4h2">')
        # save links in list
        list_of_links.append(gem_link[0])
        # save gem names in list
        gem_name_list.append((gem_link[1]))

    # open every saved link and check price
    for link in tqdm(list_of_links):
        try:
            driver.get("https://poe.ninja" + link)
            sleep(0.5)
            price_value = driver.find_element(By.XPATH, price_xpath)
            base_gems_price_list.append(price_value.text)
        except NoSuchElementException:
            print('Too fast something was skipped start over')
            base_gems_price_list.append('0')
            continue

    driver.close()
    driver.quit()


# price check for different variations
def check_gems(test_subject_link, test_subject_list):
    # chromedriver location
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(test_subject_link)
    # accept cookies once
    driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[3]/div[1]/button[2]').click()

    for gem in tqdm(gem_name_list):
        try:
            driver.get(test_subject_link)
            sleep(0.2)
            # input name
            driver.find_element(By.XPATH, '/html/body/div[3]/section/div/main/section/div/div/div/div[2]/div/div[1]/'
                                          'input').send_keys(
                str(gem))
            sleep(0.2)
            # click on result
            driver.find_element(By.XPATH, '/html/body/div[3]/section/div/main/section/div/div/div/div[3]/div/table/'
                                          'tbody/tr/td[1]/div/div/a').click()
            sleep(0.2)
            price_value = driver.find_element(By.XPATH, price_xpath)
            test_subject_list.append(price_value.text)
            sleep(0.2)
        except NoSuchElementException:
            test_subject_list.append('0')
            continue
    driver.close()
    driver.quit()


initial_names_and_price(base_gems_link)
check_gems(failed_gems_link, failed_gems_price_list)
check_gems(successful_gems_link, successful_gems_price_list)

df = pd.DataFrame({'Gem Name': gem_name_list, 'Base': base_gems_price_list, '20/20': failed_gems_price_list,
                   '21/20': successful_gems_price_list})
df.to_csv('gems_anomalous.csv', index=False, encoding='utf-8')
