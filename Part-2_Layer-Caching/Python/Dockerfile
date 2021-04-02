FROM python:3.8.5-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt 
COPY . .

EXPOSE 8080

CMD ["/bin/sh","-c","gunicorn wsgi:app"]
