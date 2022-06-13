FROM python:3.10-alpine
WORKDIR /usr/local/app
COPY . .
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers zlib-dev jpeg-dev libjpeg \
    && apk add libjpeg  \
    && apk add build-base postgresql-dev libpq  \
    && pip install Pillow --no-cache-dir  \
    && apk del .tmp
#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt &&  pip3 install gunicorn
EXPOSE 8000
CMD ["gunicorn", "server.wsgi"]