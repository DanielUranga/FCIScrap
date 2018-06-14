#!/bin/sh

cron &
python ./rest_server.py &       # Starts the RESTful server
nginx                           # Starts nginx web server
