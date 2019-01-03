FROM node:7.10.1-slim
ADD . /config
WORKDIR /config
#COPY migrations /manage/migrations
#COPY packages.json /manage/
#COPY migrate-mongo-config.js /manage/
RUN npm install
CMD ["npm", "run", "up"]