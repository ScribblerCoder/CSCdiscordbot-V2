#! /usr/bin/env python3

import os
import discord
from discord.ext import commands
import dotenv
import csv
import time

# Read a CSV file to a list of dict
reader = csv.DictReader(open('final.csv', 'r'))

dict_list = []

for line in reader:
    dict_list.append(line)


# ID list
id_ls = []
for ls in dict_list:
    id_ls.append(ls['ID'])

# Initialzie objects/values
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)


# shit legacy code btw :)
@bot.command()
async def tryharder(ctx):
    await ctx.send(f'https://www.youtube.com/watch?v=t-bgRQfeW64&ab_channel=Muh.AndryAmiruddin')


# Purge roles of members of the server. (Soft Reset)
@bot.command(pass_context=True)
@commands.is_owner()
async def purge(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Member')
    for member in ctx.guild.members:
        if member.id != bot.user.id:
            if role in member.roles:
                await ctx.send(f'{member.id}\t{member.name}')
                await member.edit(roles=[
                    discord.utils.get(ctx.guild.roles, name='Unverified'),
                    discord.utils.get(ctx.guild.roles, name='Member')
                ])
                await member.create_dm()
                await member.dm_channel.send(
                    f'If you have registered for the training please check your email to verify again. You will not be able to see your training text and voice channels until you verify.'
                )
            else:
                await member.edit(roles=[
                    discord.utils.get(ctx.guild.roles, name='Unverified')
                ])
    await ctx.send('Purging complete!')


# Lists the memeber's roles
@bot.command()
async def info(ctx):
    member = ctx.author
    roles = [i.name for i in member.roles]
    await member.create_dm()
    await member.dm_channel.send(f'You have the following roles:')
    ctr = 0
    st = '```\n'
    roles.pop(0)
    for i in roles:
        ctr += 1
        st += f'{ctr}- {i}\n'
    st += '```'
    await member.dm_channel.send(st)
    await member.dm_channel.send(f'Check the Announcements page to see the day, the time, and instructor of your training lecture.')



# For our favorite Sk1d
@bot.command()
async def skid(ctx):
    id = '<@648123560229077003>'
    await ctx.send(f'Your favorite $ʞ(!|)d3 {id}')


@bot.command()
async def verify(ctx, ID='', token=''):  # Verification

    csc_server = ctx.guild
    member = csc_server.get_member(ctx.message.author.id)

    if ctx.channel.name != 'verification':
        await member.create_dm()
        await member.dm_channel.send(f'The command !verify is not supposed to be used in {ctx.channel.name}')
        await ctx.message.delete()
        return

    if ID == '':  # Check if ID is empty
        await member.create_dm()
        await member.dm_channel.send(f'No ID given, the correct format of the command is ```!verify Student_ID Token```')
        await ctx.message.delete()
        return

    if token == '':  # Check if token is empty
        await member.create_dm()
        await member.dm_channel.send(f'No token given, the correct format of the command is ```!verify Student_ID Token```')
        await ctx.message.delete()
        return

    if ID not in id_ls:
        await member.create_dm()
        await member.dm_channel.send(f'Wrong Studnet_ID given, make sure that your Studnet_ID is correct')
        await ctx.message.delete()
        return

    for ls in dict_list:  # Find User's dictionary
        if ls['ID'] == ID:
            break

    V_token = ls['token']
    if token != V_token:
        await member.create_dm()
        await member.dm_channel.send(f'Invalid Token, try again with the correct token')
        await ctx.message.delete()
        return

    if ls['registered'] != '':
        await member.create_dm()
        await member.dm_channel.send(f'Token and ID pair have already been used.')
        await ctx.message.delete()
        return

    rm_role = discord.utils.get(csc_server.roles, name="Unverified")
    await member.remove_roles(rm_role)

    name = ls['name']
    level = ls['training']

    role = discord.utils.get(csc_server.roles, name="Member")
    await member.edit(nick=f'{name}')
    await member.add_roles(role)

    if level == 'Intermediate':
        role2 = discord.utils.get(
            csc_server.roles, name='Intermediate Student')
        await member.add_roles(role2)

    elif level == 'beginner1':
        role2 = discord.utils.get(csc_server.roles, name='Beginner Student')
        await member.add_roles(role2)
        role3 = discord.utils.get(csc_server.roles, name='Thursday')
        await member.add_roles(role3)

    elif level == 'beginner2':
        role2 = discord.utils.get(csc_server.roles, name='Beginner Student')
        await member.add_roles(role2)
        role3 = discord.utils.get(csc_server.roles, name='Saturday')
        await member.add_roles(role3)

    elif level == 'pentest':
        role2 = discord.utils.get(csc_server.roles, name='Pen-testing Student')
        await member.add_roles(role2)

    # sleep for 5 seconds to make sure all roles are given before sending them to the member
    time.sleep(5)
    ls['registered'] = 'True'
    roles = [i.name for i in member.roles]
    await member.create_dm()
    await member.dm_channel.send(f'Congrats, {member.name}. You are now an official member of the CSC discord server.\nYou were given the following roles:')
    ctr = 0
    st = '```\n'
    roles.pop(0)
    for i in roles:
        ctr += 1
        st += f'{ctr}- {i}\n'
    st += '```'
    await member.dm_channel.send(st)
    await ctx.message.delete()


@bot.event
async def on_message(message):

    if message.author != bot.user:
        try:
            if message.channel.name == 'verification' and message.content.split()[0] != '!verify':
                await message.delete()
                await message.author.create_dm()
                await message.author.dm_channel.send(f'only !verify is allowed to be used in the verification channel!')
                return
        except:
            pass

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'\n{bot.user} has connnected to Discord!\n')
    for guild in bot.guilds:
        print(
            f'''{bot.user} has connnected to the following guild:\n
        {guild.name} (id: {guild.id})
        ''')


@bot.event
async def on_member_join(member):
    csc_server = member.guild
    role = discord.utils.get(csc_server.roles, name="Unverified")
    await member.add_roles(role)
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, welcome to the official Cyber Security Club 20/21 server\nTo be able to join the server you must verify your identity. You will need to enter the command ```!verify Student_ID Token``` in the "verification" channel in the {csc_server.name}')

bot.run(TOKEN)
#Hello!
