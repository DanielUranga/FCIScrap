# Pull base image.
FROM ubuntu

# Install Nginx.
RUN \
  apt-get update && \
  apt-get install -y nginx python python-pip && \
  rm -rf /var/lib/apt/lists/* && \
  echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
  chown -R www-data:www-data /var/lib/nginx

COPY www/* /var/www/html/
COPY nginx_proxy.conf /etc/nginx/sites-enabled/

COPY rest_server.py .
COPY run.sh .
COPY requirements.txt .
COPY periodically_scrap.py .

RUN rm /etc/nginx/sites-enabled/default
RUN mkdir data
RUN chmod +x run.sh
RUN chmod +x periodically_scrap.py
RUN pip install -r requirements.txt

CMD ["sh", "-c", "./run.sh"]

# Expose ports.
EXPOSE 80
EXPOSE 443
