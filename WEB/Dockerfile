FROM python:3.6-slim
ADD . /code
WORKDIR /code
RUN pip3 install pipenv
RUN pipenv install --skip-lock
CMD ["pipenv", "run", "python", "app.py"]