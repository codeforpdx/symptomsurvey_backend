FROM node:7.10.1-slim
ADD . /manage
WORKDIR /manage
#COPY migrations /manage/migrations
#COPY packages.json /manage/
#COPY migrate-mongo-config.js /manage/
RUN npm install
CMD ["npm", "run", "up"]