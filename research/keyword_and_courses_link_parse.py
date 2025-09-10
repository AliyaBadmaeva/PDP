import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import random


date = datetime.today()
print('Сейчас ', date)

# настройки
CHROMEDRIVER_PATH = r'./webdriver/chromedriver.exe'
OUTPUT_DIR = r'C:/Users/alius/PDP/research/output'
CATALOG_URL = "https://stepik.org/catalog/310"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# запускаем браузер
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = r".\Google\Chrome\Application\chrome.exe"
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

# функции
driver.get(CATALOG_URL)
sleep(3)

# Открываем меню
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.rubricator-dropdown__toggler"))).click()
sleep(2)
links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "a.ember-view.rubricator-meta-category__link")]
KEYWORDS = [l for l in links if l]  # убираем пустые
print(f"Собрано {len(KEYWORDS)} ссылок-дисциплин")
print(KEYWORDS)

all_ids = set()


# скроллинг вниз страницы для прогрузки ссылок на все курсы
def slow_scroll(driver, pixels_per_step=300):
    while True:
        old = driver.execute_script("return window.pageYOffset;")
        driver.execute_script(f"window.scrollBy(0, {pixels_per_step});")
        sleep(random.randint(4, 6))
        if driver.execute_script("return window.pageYOffset;") == old:
            break



for url in KEYWORDS:
    print(f"Парсим: {url}")
    url = url +"?lang=ru"  # только курсы с меткой языка ru
    driver.get(url)
    sleep(random.randint(5, 8))  # чтобы не сработала блокировка при парсинге
    page = 1
    while True:
        slow_scroll(driver)  # используем фукцию для скроллинга вниз, так как стр динамическая
        cards = driver.find_elements(By.CSS_SELECTOR, ".course-card__title")
        print("Начинаем сбор ID...")
        for card in cards:
            sleep(random.randint(2, 7))
            try:
                href = card.get_attribute("href")
                print("Удалось найти ID", href)
                if href and "/course/" in href:
                    all_ids.add(int(href.split("/")[4].split("?")[0]))
            except StaleElementReferenceException:
                print("Элемент исчез, пропускаем его")
                continue

        print(f"Страница {page}: +{len(cards)} курсов, всего уникальных: {len(all_ids)}")

        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(@class,'has-icon')][.//span[text()='Далее']]")
            sleep(3)
            if next_btn.get_attribute("disabled"):
                break
            driver.execute_script("arguments[0].click();", next_btn)
            sleep(random.randint(5, 8))
            WebDriverWait(driver, 7).until(EC.staleness_of(cards[0]))

            # переход на начало страницы
            # медленный скроллинг вверх страницы после нажатия на "Далее"
            driver.execute_script("""
                            (function(){
                                var y=document.documentElement.scrollHeight, step=30, freq=15;
                                function scrollToTop(){
                                    window.scrollTo(0, y);
                                    y -= step;
                                    if(y>=0) setTimeout(scrollToTop, freq);
                                }
                                scrollToTop();
                            })();
                        """)
            sleep(1)
            page += 1  # счетчик страниц +1
        except:
            break

        if page > 999:
            break

# сохранение
file = os.path.join(OUTPUT_DIR, f"stepik_all_ids_{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx")
pd.DataFrame(sorted(all_ids), columns=["ID курса"]).to_excel(file, index=False)
print(f"{len(all_ids)} ID курсов: {file}")

date = datetime.today()
print('Сейчас ', date)
driver.quit()