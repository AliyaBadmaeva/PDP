import os
import pandas as pd
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


import random

CHROMEDRIVER_PATH = r'./webdriver/chromedriver.exe'
OUTPUT_DIR = r'./output'
WEBDRIVERWAIT_TIMEOUT = 300
date = datetime.today()
print('Сейчас ', date)
# Запуск браузера
service = Service(executable_path=CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Users\alius\PDP\research\Google\Chrome\Application\chrome.exe"
options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')
IDS_FILE = os.path.join(OUTPUT_DIR, 'stepik_all_ids_2025-09-07_14-34-24.xlsx')
course_ids = pd.read_excel(IDS_FILE, engine='openpyxl')['ID курса'].dropna().astype(int).tolist()
print(f'Загружено {len(course_ids)} ID курсов из {IDS_FILE}')
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

data = []

sleep(5)
def parse_course(course_id):
    url = f"https://stepik.org/course/{course_id}/reviews"
    print(f"Начинаем парсинг: {url}")
    driver.get(url)
    sleep(5)

    unique_reviews = set()
    same_count = 0

    def scroll_to_last_review():
        cards = driver.find_elements(By.CSS_SELECTOR, ".course-review-card")
        if cards:
            driver.execute_script("arguments[0].scrollIntoView();", cards[-1])
            sleep(2)

    while True:
        scroll_to_last_review()
        try:
            wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".course-review-card")) > unique_reviews)
        except:
            same_count += 1
            if same_count >= 3:
                print("Новые отзывы не подгружаются. Завершаем сбор.")
                break
            continue

        same_count = 0
        cards = driver.find_elements(By.CSS_SELECTOR, ".course-review-card")

        print(f"Обработано отзывов: {len(unique_reviews)}")


        for card in cards:
            review_id = card.get_attribute("data-review-id")
            if not review_id or review_id in unique_reviews:
                continue
            unique_reviews.add(review_id)

            colored_stars = card.find_elements(By.CSS_SELECTOR, ".colored-star")
            stars_count = len(colored_stars)
            print("Количество звёзд:", stars_count)
            try:
                text_elem = card.find_element(By.CSS_SELECTOR, ".course-review-card__text .show-more__content")
                text = text_elem.text.strip()
                print("Текст отзыва:", text)
            except:
                text = "[текст не найден]"
            # добавляем в словарь
            data.append({
                 "Курс": url.split("/")[4],  # ID курса из URL
                 "ID отзыва": review_id,
                 "Звёзды": stars_count,
                 "Отзыв": text
                })

            print(f"Обработано уникальных отзывов: {len(data)}")

            if len(cards) == 0:
                print("Отзывов не обнаружено.")

                break

#Парсим каждый курс с задержкой
for i, course_id  in enumerate(course_ids):
    parse_course(course_id)
    if i < len(course_ids) - 1:
        delay = random.randint(20, 50)
        print(f"Ожидание {delay} секунд перед следующим курсом...")
        sleep(delay)

# Сохранение в Excel
os.makedirs(OUTPUT_DIR, exist_ok=True)
filename = f"stepik_all_reviews_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
filepath = os.path.join(OUTPUT_DIR, filename)

df = pd.DataFrame(data)
df.to_excel(filepath, index=False, engine='openpyxl')

print(f"Сохранено {len(data)} уникальных курсов в:")
print(filepath)
date = datetime.today()
print('Сейчас ', date)
driver.quit()