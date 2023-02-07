FROM python:3
FROM gorialis/discord.py

WORKDIR /app

COPY src/ ./

RUN chmod +x run.sh

