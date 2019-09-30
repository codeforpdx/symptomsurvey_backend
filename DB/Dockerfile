FROM python:3.6-slim

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.name="symptomsurvey_backed/DB"
LABEL org.label-schema.description="Scripts for setting up the database used by the other sections of project"
LABEL org.label-schema.url="http://www.codeforpdx.org/projects/2"
LABEL org.label-schema.vcs-url="https://github.com/codeforpdx/symptomsurvey_backend"

WORKDIR /usr/src/app

#do this BEFORE copying the rest, that way only changes to requirements.txt will cause pip to execute
RUN pip install --upgrade pip
RUN pip3 install pymongo

ADD setup_mongo.py /
CMD ["python", "./setup_mongo.py"]
