FROM python:3.6-slim

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.name="symptomsurvey_backed/DB"
LABEL org.label-schema.description="Scripts for setting up the database used by the other sections of project"
LABEL org.label-schema.url="http://www.codeforpdx.org/projects/2"
LABEL org.label-schema.vcs-url="https://github.com/codeforpdx/symptomsurvey_backend"

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip3 install pymongo

COPY ./MANAGE /MANAGE
COPY ./SHARED/modules/common.py /MANAGE/common.py
COPY ./SHARED/json /SHARED/json
CMD ["python", "/MANAGE/setup_mongo.py"]
