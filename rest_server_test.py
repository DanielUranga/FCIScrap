import rest_server
from multiprocessing import Process
import time
import unittest
import os
import signal
import requests
import csv
import json

def run_server():
    rest_server.app.run()

def convert_date(date_in):
    tmp = date_in.split('/')
    return tmp[2] + '-' + tmp[1] + '-' + tmp[0]

class TestMoneyValue(unittest.TestCase):

    base_url = 'http://127.0.0.1:5000/money_value'

    def test_connect_with_no_args(self):
        response = requests.get(self.base_url)
        self.assertNotEqual(response.status_code, 200)

    def test_connect(self):
        response = requests.get(self.base_url,\
                                data = {'start_date':'2017-01-03',\
                                        'start_value':'100',\
                                        'end_date':'2018-01-03'\
                                        }\
                                )
        self.assertEqual(response.status_code, 200)

    def test_returns_correct(self):
        start_date = ''
        start_value = 0
        end_date = ''
        end_value = 0
        with open('data/inflation_data.csv', 'r') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            headers = next(read)[1:]
            row = next(read)
            real_money_value = 1420
            start_date = convert_date(row[0])
            start_value = int(real_money_value * float(row[1]))
            for i in range(0, 365): # Skip one year
                next(read)
            row = next(read)
            end_date = convert_date(row[0])
            end_value = int(real_money_value * float(row[1]))

        response = requests.get(self.base_url,\
                                data = {'start_date':start_date,\
                                        'start_value':str(start_value),\
                                        'end_date':end_date\
                                        }\
                                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), end_value)

    def test_returns_error_on_date_with_no_data(self):
        response = requests.get(self.base_url,\
                                data = {'start_date':'1915-01-03',\
                                        'start_value':'100',\
                                        'end_date':'2500-01-03'\
                                        }\
                                )
        self.assertNotEqual(response.status_code, 200)

    def test_returns_error_on_start_after_end(self):
        response = requests.get(self.base_url,\
                                data = {'start_date':'2017-01-03',\
                                        'start_value':'100',\
                                        'end_date':'2017-01-02'\
                                        }\
                                )
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    server = Process(target = run_server)
    server.start()
    time.sleep(1)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMoneyValue)
    unittest.TextTestRunner(verbosity=2).run(suite)

    os.kill(server.pid, signal.SIGTERM)
