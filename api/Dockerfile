FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt update && apt install gcc
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

CMD ["uvicorn",  "--reload",  "--host", "0.0.0.0",  "--port", "8000", "src.main:api"]
