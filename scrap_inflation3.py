#!/bin/env python

import subprocess
from bs4 import BeautifulSoup
import csv
import datetime
from datetime import date
import time
from datetime import timedelta
import urllib

today_url_encoded = urllib.quote_plus(date.today().strftime('%d/%m/%Y'))
html = urllib.urlopen(
    'http://www.bcra.gov.ar/PublicacionesEstadisticas/Principales_variables_datos.asp',
    'desde=31%2F03%2F2016&hasta='+today_url_encoded+'&fecha=Fecha_Cvs&descri=22&campo=Cvs&primeravez=1&alerta=5'
)
soup = BeautifulSoup(html, 'html.parser')

table = soup.select('#tabla')[0]
rows = table.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.insert(0, [ele for ele in cols if ele])

with open('data/inflation_data.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['date', 'value'])
    writer.writeheader()
    consecutive_date = None
    for row in data:
        if not row:
            continue
        st_time = time.strptime(row[0], '%d/%m/%Y')
        date = datetime.date(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)
        if consecutive_date == None:
            consecutive_date = date
        while consecutive_date < date:
            consecutive_date = consecutive_date + timedelta(days=1)
            float_val = float(row[1].replace(',', '.'))
            writer.writerow({'date': consecutive_date.strftime('%d/%m/%Y'), 'value': float_val})
