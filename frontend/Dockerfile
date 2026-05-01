FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Expone puerto de Next
EXPOSE 3000

CMD ["npm", "run", "dev"]