FROM python:3.13-alpine
LABEL authors="amedix"

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "-u", "main.py"]