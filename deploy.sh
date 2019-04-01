#!/bin/bash

NAME="capstone"
echo 'Building capstone project...'
docker build -t $NAME .
echo 'Done! Successfully build docker image'
if [ `docker ps -aq --filter name=$NAME | wc -l` -gt 0 ]; then
    echo 'Found running instance of capstone project:$(docker ps | grep $NAME)'
    CONTAINERID=$(docker ps -aq --filter name=$NAME)
    docker stop $CONTAINERID && docker rm $CONTAINERID
    echo 'Stopped and removed docker container(${CONTAINERID}, with name: ${NAME})'
fi
echo 'Starting new docker container with latest capstone build'
docker run -p 5555:5555 --name $NAME -d $NAME:latest
URL_PORT=$(docker ps --filter name=$NAME --format "table {{.Ports}}" | awk 'FNR==2 {print $1}')
STATUS=$(docker ps --filter name=$NAME --format "table {{.Status}}" | awk 'FNR==2 {print $1, $2, $3}')
echo 'Running on : ${URL_PORT}'
echo 'Status     : ${STATUS}'
echo 'Done! You should be ready to go by now'
