FROM python:3

 ENV PYTHONUNBUFFERED 1
 
 RUN mkdir /codeBoohub
 WORKDIR /codeBoohub
 
 ADD requirements.txt /codeBoohub/
 RUN pip install -r requirements.txt
 ADD . /codeBoohub/

EXPOSE 8027

