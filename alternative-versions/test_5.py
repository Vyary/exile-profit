from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import multiprocessing as mp


def worker(url):
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    driver.get(url)
    # do the necessary operations
    # task1; task2; task3
    # close instance after completed
    driver.quit()


url_list = ["https://github.com/Aqua-4/auto-insta/blob/master/refresh_db.py",
            "https://stackoverflow.com/questions/59706118/how-to-run-multiple-selenium-drivers-parallelly",
            'https://www.craftofexile.com/',
            'https://www.nike.com/bg/w/new-mens-shoes-3n82yznik1zy7ok?sort=newest']

if __name__ == '__main__':
    p = mp.Pool(mp.cpu_count())
    p.map(worker, url_list)
