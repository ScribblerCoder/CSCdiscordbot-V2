#!/bin/bash 

python3 generate.py

docker rm container -f cscbot
docker image rm -f cscbot
docker build -t cscbot:latest . 
docker run -d --name cscbot -it cscbot:latest
