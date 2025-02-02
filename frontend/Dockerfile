FROM node:16

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . /app/

RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "5000"]

EXPOSE 5000
