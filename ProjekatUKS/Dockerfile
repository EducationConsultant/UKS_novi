 FROM python:3

 ENV PYTHONUNBUFFERED 1
 
 RUN mkdir -p /usr/src/boohub
 WORKDIR /usr/src/boohub
 
 
 COPY requirements.txt .
 RUN pip install -r requirements.txt

 RUN mkdir -p myappBoohub
 COPY ./myappBoohub ./myappBoohub

 RUN mkdir -p myappBoohub/logs

 EXPOSE 8027
 
 
 
