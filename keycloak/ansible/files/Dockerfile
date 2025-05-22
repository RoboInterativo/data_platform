# Build Stage
FROM node:20.18.1-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production Stage
EXPOSE 8080 5000
CMD [ "node", "build/server.js" ]