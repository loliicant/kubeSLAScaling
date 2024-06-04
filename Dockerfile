FROM python:3.8.10
 
WORKDIR /app

COPY . /app
 
RUN pip3 install flask
RUN pip3 install kubernetes
RUN pip3 install opentelemetry-api
RUN pip3 install opentelemetry-sdk
EXPOSE 5000 
 
CMD python3 app.py
