FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt update -y && apt install gcc python3-all python3 python3-pip -y
COPY requirements.txt /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY linux-only-requirements.txt /app/
RUN pip3 install -r linux-only-requirements.txt

COPY . /app

#CMD ["uvicorn", "--help"]
CMD ["uvicorn", "--reload", "--host", "0.0.0.0",  "--port", "8000", "src.main:api"]
