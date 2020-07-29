FROM python:alpine3.7

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN chmod +x ./run.sh 

ENTRYPOINT ./run.sh