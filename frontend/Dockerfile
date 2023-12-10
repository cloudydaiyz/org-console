FROM node:21-alpine

ENV APP_PORT=80

WORKDIR /app

COPY . .

EXPOSE $APP_PORT

RUN ["npm", "install"]

CMD ["npm", "start"]