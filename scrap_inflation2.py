from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import subprocess
import csv
import re
import json
import datetime
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
page = driver.get('http://estadisticasbcra.com/unidad_de_valor_adquisitivo')

p_element = driver.find_element_by_xpath('/html/body/main/script')
token = re.search('var jsToken = "([a-zA-Z0-9._-]+)";', p_element.get_attribute('innerHTML')).group(1)

print(token)

command = [
    'curl',
    'http://api.estadisticasbcra.com/uva',
    '-H', 'Host: api.estadisticasbcra.com',
    '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    '-H', 'Accept: application/json,*/*" -H "Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    '--compressed',
    '-H', 'Referer: http://estadisticasbcra.com/unidad_de_valor_adquisitivo',
    '-H', "authorization: Bearer {0}".format(token),
    '-H', 'Origin: http://estadisticasbcra.com',
    '-H', 'Connection: keep-alive',
    '--silent'
]
data = json.loads(subprocess.check_output(command))
with open('data/inflation_data.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['date', 'value'])
    writer.writeheader()
    for row in data:
        st_time = time.strptime(row['d'].replace('\'', '').replace('u', ''), '%Y-%m-%d')
        date = datetime.date(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)
        writer.writerow({'date': date.strftime('%d/%m/%Y'), 'value': row['v']})

driver.close()
