#!/bin/bash 


docker rm container -f cscbot
docker image rm -f cscbot
docker build -t cscbot:latest . 
docker run -d -v $(pwd)/data:/app/data --name cscbot -it cscbot:latest
