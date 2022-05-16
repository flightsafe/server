FROM python:3.10-slim
WORKDIR /usr/local/app
COPY . .
#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
EXPOSE 8000

CMD ["gunicorn", "server.wsgi"]