FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python","main.py"]