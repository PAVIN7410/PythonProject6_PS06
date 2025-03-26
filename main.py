import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Настройки для работы с драйвером
options = Options()
options.headless = False  # Установите True, если не нужно открывать браузер
service = Service(executable_path='C:\\Windows\\chromedriver-win64\\chromedriver.exe')  # Укажите путь к chromedriver

# Инициализация драйвера
driver = webdriver.Chrome(service=service, options=options)
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)
time.sleep(3)

# Находим все вакансии
vacancies = driver.find_elements(By.CSS_SELECTOR, 'div.magritte-card___bhGKz_7-0-4')
print(vacancies)

parsed_data = []

# Обходим найденные вакансии
for vacancy in vacancies:
    try:
        # Получаем заголовок вакансии
        title_element = vacancy.find_element(By.CSS_SELECTOR,'span[data-qa="serp-item__title-text"]')
        title = title_element.text
        link = title_element.get_attribute('href')

        # Получаем название компании

        company_element = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-employer-text"]')

        company = company_element.text

        # Получаем зарплату
        try:

            salary_element = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-compensation"]')

            salary = salary_element.text
        except Exception:
            salary = "Не указана"

        # Добавляем данные в список
        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print(f"Произошла ошибка при парсинге вакансии: {e}")
        continue

# Печатаем количество найденных вакансий
print(f"Найдено вакансий: {len(vacancies)}")

# Завершаем работу драйвера
driver.quit()

# Записываем данные в CSV файл
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)
print(f"Записано {len(parsed_data)} вакансий в файл vacancies.csv")
print("Данные успешно записаны в hh.csv")



