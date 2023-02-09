FROM python:3
FROM gorialis/discord.py

WORKDIR /app

COPY src/ ./

RUN pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib

ENTRYPOINT ["python3","bot.py"]

