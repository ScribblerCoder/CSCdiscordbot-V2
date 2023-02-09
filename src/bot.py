#! /usr/bin/env python3
from __future__ import print_function

import os
import json
import sys
import time
import sqlite3
import uuid

import discord
from discord.ext import commands, tasks




from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


# initialize sqlite db
connection = sqlite3.connect("/app/data/members_database.db")
cursor = connection.cursor()
cursor.execute(
            'CREATE TABLE IF NOT EXISTS members (name text, email text, id int primary key unique, class text, token text unique, registered bool, email_sent bool)'
        )
connection.commit()


# initialize discord bot
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=config["bot_prefix"],
    intents=intents
    )
    

# discord events and tasks

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break

    print(f'{bot.user} is connected to the following guild:\n'
    f'{guild.name} (id: f{guild.id})')
    sync_db.start() # start the task to update db every minute

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, Welcome to the official Cyber Security Club server\nTo be able to join the server you must verify your identity. You will need to enter the command ```!verify Student_ID Token``` here in the direct message channel.')

@tasks.loop(seconds=60)
async def sync_db():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1-JEKV1K6EUsjD_ySjdOiAfw0P5Do3_no56xzcgLT9n8'
    SAMPLE_RANGE_NAME = 'B2:K500'



    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('Sheet is empty')

        else:
            print("Syncing with db....")
            print(f'Inserting {len(values)} records')
            for row in values:
                # Add members into db
                cursor.execute('''INSERT OR IGNORE INTO members(
                   name,email,id,class,token,registered,email_sent) VALUES 
                   (?,?,?,?,?,?,?)''',(row[0],row[1],int(row[2]),row[3],str(uuid.uuid4()),0,0) ) 
                connection.commit()

    except HttpError as err:
        print(err)
 

# discord commands

@bot.command(name='bully_nizar')
async def bully_nizar(ctx, ID='',token=''):
    await ctx.send(f'nizar nizar nizar niz niz niz niz nizaaaar..... please buy tickets :)')
    return

@bot.command(name='verify')
async def verify(ctx, ID='', token=''):

    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break

    member = guild.get_member(ctx.message.author.id)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await member.create_dm()
        await member.dm_channel.send(f'The command `!verify` can only be used in a direct message channel.')
        await ctx.message.delete()
        return
        
    if ID == '':  # Check if ID is empty
        await ctx.send(f'No ID given, the correct format of the command is \n`!verify Student_ID Token`')
        return

    if token == '':  # Check if token is empty
        await ctx.send(f'No Token given, the correct format of the command is \n`!verify Student_ID Token`')
        return


    # search for the member's record
    rows = cursor.execute(
        "SELECT * FROM members WHERE id = ?",
        (ID,),
    ).fetchall()

    if len(rows) == 0:  # Check if ID exists 
        await ctx.send(f'Wrong Student_ID given, make sure that your Student_ID is correct')
        return
    
    if token != rows[0][3]:   # Check if token is invalid
        await ctx.send(f'Invalid Token, make sure that your Token is correct')
        return
    
    if rows[0][4]:  # Check if user has registered previously
        await ctx.send(f'Token and ID pair have already been used.')
        return
    
    name = rows[0][1]
    level = rows[0][2]
    roles = ['Member']

    # not sure why's this if-statment for?
    if len(name) > 32:
        name = name.split()[0] + ' ' + name.split()[1]
        name = name.split()[0]

    await member.edit(nick=f'{name}')

    role = discord.utils.get(guild.roles, name="Member")
    await member.add_roles(role)
    
    if level != 'None':
        role = discord.utils.get(guild.roles, name=level)
        await member.add_roles(role)
        roles.append(level)


    time.sleep(5)   # doing all these checks is tiring so I need to rest hahaha

    cursor.execute(
        "UPDATE members SET registered = TRUE WHERE id = ?",
        (ID,)
    )
    connection.commit()

    st = '```\n'
    for i in roles:
        ctr += 1
        st += f'{ctr}- {i}\n'
    st += '```'

    embed=discord.Embed(title="Welcome!", description=f"You are now an official member of the CSC discord server.\nYou were given the following roles:\n {st}", color=0xFF5733)
    embed.set_image(url="https://i.pinimg.com/originals/be/97/2b/be972b4214bb16fc4a088b9f73c18717.jpg")
    await ctx.send(embed=embed)

    # await ctx.send(f'Congrats, {member.name}. You are now an official member of the CSC discord server.\nYou were given the following roles:\n')
    # ctr = 0
    # st = '\n`'
    # for i in roles:
    #     ctr += 1
    #     st += f'{ctr}- {i}\n'
    # st += '`'
    # await ctx.send(st)

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, Welcome to the official Cyber Security Club server\nTo be able to join the server you must verify your identity. You will need to enter the command ```!verify Student_ID Token``` here in the direct message channel.')


bot.run(config["token"], reconnect=True)