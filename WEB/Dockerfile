FROM python:3.6-slim

WORKDIR /usr/src/app

ADD ./WEB .
ADD ./SHARED .

RUN pip3 install pipenv
RUN pipenv install --skip-lock

CMD ["pipenv", "run", "python", "app.py"]