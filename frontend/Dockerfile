FROM node:18.9-alpine3.15 as build

WORKDIR /app

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
RUN npm i

COPY . /app
ENV CI=true
ENV PORT=3000
RUN npm run build

FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /usr/share/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*
COPY --from=build /app/build .

EXPOSE 80 443
# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]