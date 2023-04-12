FROM node:14

ENV CI=true
ENV PORT=5000 

WORKDIR /code
COPY package.json /code/package.json
COPY package-lock.json /code/package-lock.json
RUN npm ci
COPY . /code

CMD ["npm", "start"]
