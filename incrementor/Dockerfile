FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app

COPY requierments.txt /app/requierments.txt

RUN pip install -r /app/requierments.txt

EXPOSE 8080

ENV REDIS_SERVER localhost
ENV REDIS_PORT 6379

COPY app.py /app

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "app:app"]
