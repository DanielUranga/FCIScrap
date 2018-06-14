# Pull base image.
FROM ubuntu

# Install Nginx.
RUN \
  apt-get update && \
  apt-get install -y nginx python python-pip cron && \
  rm -rf /var/lib/apt/lists/* && \
  echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
  chown -R www-data:www-data /var/lib/nginx

COPY www/* /var/www/html/
COPY nginx_proxy.conf /etc/nginx/sites-enabled/

COPY rest_server.py .
COPY scrap_inflation3.py .
COPY scrap.sh .
COPY run.sh .
COPY requirements.txt .

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/simple-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

RUN rm /etc/nginx/sites-enabled/default
RUN mkdir data
RUN chmod +x scrap.sh
RUN chmod +x run.sh
RUN pip install -r requirements.txt

CMD ["sh", "-c", "./run.sh"]

# Expose ports.
EXPOSE 80
EXPOSE 443
