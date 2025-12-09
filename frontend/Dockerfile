# Сборка фронтенда
FROM node:18-alpine as build-stage
WORKDIR /app
COPY frontend/ .
RUN npm install
RUN npm run build

# Продакшн сервер
FROM nginx:alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
