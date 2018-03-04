# Inflacion verdadera no tiene mas datos para Argentina :'(. Seguramente tiene
# que ver con que la inflacion se esta acelerando y al ser pro-Macri no quieren
# que quede en evidencia.

from selenium import webdriver
import csv
import datetime
import time

driver = webdriver.PhantomJS()
page = driver.get('http://www.inflacionverdadera.com/argentina/')

p_element = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/article/div/div/div/div/div/div[5]/div/div/div[3]/div/div/div/div/div[1]/div/div/table/tbody')

with open('data/inflation_data.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['date', 'value'])
    writer.writeheader()
    for trs in p_element.find_elements_by_tag_name('tr'):
        tds = trs.find_elements_by_tag_name('td')
        st_time = time.strptime(tds[0].get_attribute('innerHTML'), '%d%b%Y')
        date = datetime.date(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)
        price_data = tds[1].get_attribute('innerHTML').replace(',', '')
        writer.writerow({'date': date.strftime('%d/%m/%Y'), 'value': price_data})
