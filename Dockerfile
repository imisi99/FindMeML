FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x generate.sh && ./generate.sh

EXPOSE 8000

CMD [ "python", "main.py" ]
