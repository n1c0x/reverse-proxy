FROM nginx
STOPSIGNAL 3

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


CMD service nginx start && tail -F /var/log/nginx/error.log