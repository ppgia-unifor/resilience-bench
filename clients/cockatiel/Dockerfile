FROM node:19.9.0 as build

WORKDIR /home/node/app

COPY . .
RUN npm ci
RUN npm run build

FROM node:19.9.0-alpine3.17

WORKDIR /home/node/app

COPY --chown=node:node ./package.json .
COPY --chown=node:node ./package-lock.json .
COPY --from=build --chown=node:node /home/node/app/build .

RUN npm ci --production
EXPOSE 80
CMD ["node", "index.js"]