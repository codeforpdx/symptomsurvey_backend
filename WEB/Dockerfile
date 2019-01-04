FROM python:3.6-slim

WORKDIR /usr/src/app

ADD ./WEB .
ADD ./SHARED .

RUN pip3 install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]