FROM node:7.10.1-slim

WORKDIR /usr/src/app

#do this BEFORE copying the rest, that way only changes to package.json will cause npm to execute
COPY ./MANAGE/package.json ./package.json
RUN npm install

COPY ./MANAGE ./SHARED ./
