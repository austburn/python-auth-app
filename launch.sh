#!/bin/bash

app_running=$(docker ps --filter "name=python-auth-app" --filter "status=running" -q | wc -l)
app_exited=$(docker ps --filter "name=python-auth-app" --filter "status=exited" -q | wc -l)

db_running=$(docker ps --filter "name=python-auth-db" --filter "status=running" -q | wc -l)
db_exited=$(docker ps --filter "name=python-auth-db" --filter "status=exited" -q | wc -l)

if [ "$app_exited" -eq 1 ]; then
    docker rm -f python-auth-app
fi

if [ "$db_exited" -eq 1 ]; then
    docker rm -f python-auth-db
fi

if [ "$db_running" -eq 0 ]; then
    docker run -d --name python-auth-db -e POSTGRES_USER=austburn -e POSTGRES_PASSWORD=pass1234 postgres
fi

if [ "$app_running" -eq 0 ]; then
    docker run -it --name python-auth-app --link python-auth-db:postgres python-auth-app
fi
