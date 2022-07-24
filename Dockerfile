FROM python:3.8

WORKDIR /fastapi-app 

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . ./fastapi-app

CMD ["python", ".fastapi-app/app/main.py"]

EXPOSE 8000