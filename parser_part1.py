from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sqlite3

# Настраиваем драйвер
chrome_driver_path = r'C:\chromedriver-win64\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')  # Запустим в фоновом режиме
chrome_options.add_argument('window-size=640,480')
chrome_options.add_argument('--disable-extensions')  # Отключает расширения
chrome_options.add_argument('--disable-infobars')

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL страницы входа и страницы с данными
login_url = r'https://admin.biletyna.pl/auth'
data_url = r'https://admin.biletyna.pl/instructor-app/course/view/60456'

# Открываем страницу входа
driver.get(login_url)

# login =
# password =

# Заполняем форму
driver.find_element(By.ID, 'login').send_keys('mirsantaki.20@gmail.com')
driver.find_element(By.ID, 'pass').send_keys('rock24Ka')

# Отправляем форму
driver.find_element(By.ID, 'pass').send_keys(Keys.RETURN)

# Явное ожидание загрузки следующей страницы
WebDriverWait(driver, 10).until(EC.url_changes(login_url))

# Открываем страницу с данными
driver.get(data_url)

# Явное ожидание загрузки таблицы
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'customer_record')))

# Получаем HTML содержимое
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Находим таблицу
table = soup.find('table', class_='table table-responsive table-hover')

# Находим все строки таблицы
rows = table.find_all('tr', class_='customer_record')

# Список для хранения данных
records = []

# Обрабатываем каждую строку
for row in rows:
    cols = row.find_all('td')  # Находим все ячейки в строке
    record = {
        'User': cols[0].text.strip(),
        # 'Grupa': cols[1].text.strip(),
        # 'Należność brutto': cols[2].text.strip(),
        # 'Należność netto': cols[3].text.strip(),
        # 'Zapłacono brutto': cols[4].text.strip(),
        # 'Zapłacono netto': cols[5].text.strip(),
        'Debt': cols[6].text.strip()[:-6],
    }
    records.append(record)

driver.quit()

connection = sqlite3.connect(r'C:\Users\user\Desktop\SQLite\contacts.db')
cursor = connection.cursor()

# debt_list = []

for i in records:
    cursor.execute('''
        UPDATE contacts
        SET debt = ?
        WHERE name_in_db = ?
        ''', (i['Debt'], i['User']))

connection.commit()

if cursor.rowcount == 0:
    print('Record not found')
else:
    print('Success')

connection.close()

with open(r'C:\Users\user\Desktop\python\debts.txt', 'a') as f:
    f.write('\n' + time.ctime() + '\n' + '\n')

    for i in records:
        if i['Debt'] != '0,00':
            f.write(str(i) + '\n')
