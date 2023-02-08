FROM python:3
FROM gorialis/discord.py

WORKDIR /app

COPY src/ ./

ENTRYPOINT ["python3","bot.py"]

