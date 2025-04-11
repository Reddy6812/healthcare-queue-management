FROM node:16-alpine

WORKDIR /app

COPY package.json .
COPY package-lock.json .  # if you use package-lock

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
