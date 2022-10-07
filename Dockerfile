FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /app
WORKDIR /app

COPY . .


RUN chmod +x script.sh
