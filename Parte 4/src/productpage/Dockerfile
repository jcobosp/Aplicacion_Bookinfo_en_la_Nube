FROM python:3.8.10

RUN apt-get update
RUN apt-get install -y python3-pip
 
WORKDIR /opt/microservices/

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 9080

CMD ["python3", "productpage.py", "9080"]
