FROM python:3.8.10

RUN apt-get update
RUN apt-get install -y python3-pip

COPY ./practica_creativa2/bookinfo/src/productpage .

RUN pip3 install -r requirements.txt

EXPOSE 9080
 
CMD ["python3", "productpage_monolith.py", "9080"]
