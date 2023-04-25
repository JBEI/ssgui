# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:16 as build-stage

WORKDIR /app

COPY package.json package-lock.json /app/

RUN npm install

COPY ./ /app/

RUN npm run build


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:mainline-alpine

COPY --from=build-stage /app/dist/ /usr/share/nginx/html
COPY ./nginx-serve-diva.conf /etc/nginx/conf.d/default.conf
