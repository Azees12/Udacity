FROM python:3.7.2-slim

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt


CMD ["gunicorn", "-b", ":8080", "main:APP"]
