FROM python:3.9-slim

EXPOSE  5000
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . .
CMD python app.py