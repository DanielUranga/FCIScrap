import urllib2
import datetime
import time
import json
import csv

from datetime import timedelta

def plus_one_month(date):
    new_date = date
    while date.month == new_date.month:
        new_date += timedelta(days=1)
    while date.day != new_date.day:
        new_date += timedelta(days=1)
    return new_date

def download_month(date, fondo_id, clase_id):
    str_month_start = date.strftime('%Y-%m-%d')
    str_month_end = plus_one_month(date).strftime('%Y-%m-%d')
    url = "http://api.cafci.org.ar/fondo/{0}/clase/{1}/rendimiento/{2}/{3}?step=1".format(fondo_id, clase_id, str_month_start, str_month_end)
    print('Going to request: ' + url)
    data = json.load(urllib2.urlopen(url))
    retval = []
    if 'success' in data and data['success']:
        for range in data['data']:
            hasta = range['hasta']
            retval.append({'date': hasta['fecha'], 'value': hasta['valor']})
        print 'Success'
    else:
        print 'download_month: {0} failed'.format(str_month_start)
    return retval

def download_all(date, fondo_id, clase_id, retval):
    while date < datetime.date.today():
        arr = download_month(date, fondo_id, clase_id)
        for new_elem in arr:
            should_add = True
            for old_elem in retval:
                if new_elem['date'] == old_elem['date']:
                    should_add = False
                    assert(new_elem['value'] == old_elem['value'])
            if should_add:
                retval.append(new_elem)
        date = plus_one_month(date)
    return retval

def download_and_write_to_file(fondo_id, clase_id):
    filename = 'data/fondo_{0}_clase_{1}.csv'.format(fondo_id, clase_id)
    existent = []
    most_recent = datetime.date(2016, 1, 1)
    try:
        with open(filename, 'rb') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            headers = next(read)[1:]
            for row in read:
                st_time = time.strptime(row[0], '%d/%m/%Y')
                row_time = datetime.date(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)
                if row_time > most_recent:
                    most_recent = row_time
                existent.append({'date': row_time.strftime('%d/%m/%Y'), 'value': row[1]})
    except IOError:
        print('{0} does not exists, going to download all data and create it').format(filename)

    data = download_all(most_recent, fondo_id, clase_id, existent)
    with open(filename, 'w') as csvfile:
        fieldnames = ['date', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

download_and_write_to_file(151, 151)
