FROM node:19.9.0-alpine3.17
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY package.*json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD [ "npm", "start"]
