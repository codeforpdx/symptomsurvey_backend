FROM python:3.6-slim

WORKDIR /usr/src/app

#do this BEFORE copying the rest, that way only changes to requirements.txt will cause pip to execute
ADD ./WEB/requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

ADD ./WEB ./SHARED ./

CMD ["flask", "run", "--host=0.0.0.0"]
