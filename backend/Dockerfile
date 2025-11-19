FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["sh", "-c", "sleep 5 && python3 app.py && python3 insert_seed.py"]
