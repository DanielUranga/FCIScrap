from selenium import webdriver
import subprocess
import csv
import re
import json

driver = webdriver.PhantomJS()
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
print(data)
