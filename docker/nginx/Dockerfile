# The first stage
# Build React static files
FROM node:13.12.0-alpine as build

WORKDIR /app/nfl-rushing-fe
COPY ./nfl-rushing-fe/package.json ./
COPY ./nfl-rushing-fe/package-lock.json ./
RUN npm ci --silent
COPY ./nfl-rushing-fe/ ./
RUN npm run build

# The second stage
# Copy React static files and start nginx
FROM nginx:stable-alpine
COPY --from=build /app/nfl-rushing-fe/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]