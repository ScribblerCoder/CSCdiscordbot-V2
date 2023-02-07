#! /usr/bin/env python3
import os
import json
import sys
import time
import sqlite3
import uuid

import discord
from discord.ext import commands, tasks


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


connection = sqlite3.connect("/app/data/members_database.db")
cursor = connection.cursor()
cursor.execute(
            'CREATE TABLE IF NOT EXISTS members (id int, name text, class text, token text, registered bool)'
        )
connection.commit()


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=config["bot_prefix"],
    intents=intents
    )
    



@bot.event
async def on_ready():
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break

    print(f'{bot.user} is connected to the following guild:\n'
    f'{guild.name} (id: f{guild.id})')

    

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

    if rows.len() == 0:  # Check if ID exists 
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

    await ctx.send(f'Congrats, {member.name}. You are now an official member of the CSC discord server.\nYou were given the following roles:\n')
    ctr = 0
    st = '\n`'
    for i in roles:
        ctr += 1
        st += f'{ctr}- {i}\n'
    st += '`'
    await ctx.send(st)

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, Welcome to the official Cyber Security Club server\nTo be able to join the server you must verify your identity. You will need to enter the command ```!verify Student_ID Token``` here in the direct message channel.')


bot.run(config["token"], reconnect=True)