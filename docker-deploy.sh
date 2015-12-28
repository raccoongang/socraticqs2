#!/usr/bin/env sh

echo "Deploying project."

docker-compose stop web
docker-compose rm -f web
docker rmi -f socraticqs2_web
docker-compose up -d web

echo "Done."
