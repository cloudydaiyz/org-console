FROM node:21-alpine

ARG PORT

ENV APP_PORT=8080

WORKDIR /app

COPY . .

EXPOSE $APP_PORT

RUN ["npm", "install"]

CMD ["npm", "start"]