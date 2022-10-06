#!/bin/bash 

docker rm -f cscbot 
docker build -t cscbot:latest . 
docker run -d --name cscbot -it cscbot:latest
