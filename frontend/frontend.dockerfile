FROM node:19

WORKDIR /frontend

COPY . .

RUN npm install