FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN unzip final.zip

RUN chmod +x script.sh
