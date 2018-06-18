#!/bin/sh

python ./periodically_scrap.py &
python ./rest_server.py &         # Starts the RESTful server
nginx                             # Starts nginx web server
