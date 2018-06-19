#!/bin/env python

import schedule
import time
import subprocess

def job():
    subprocess.call(["python", "./scrap_inflation3.py"])

schedule.every(30).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
