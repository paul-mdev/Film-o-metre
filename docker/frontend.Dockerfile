# docker/frontend.Dockerfile

# Étape 1 : construire l'app
FROM node:18 AS build
WORKDIR /app
COPY . .
RUN npm install

RUN npm run build

# Étape 2 : servir avec un serveur statique (nginx)
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
