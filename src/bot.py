#! /usr/bin/env python3
from __future__ import print_function

import os
import json
import sys
import time
import sqlite3
import uuid
import base64

import discord
from discord.ext import commands, tasks


from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
            'CREATE TABLE IF NOT EXISTS members (name text, email text, id int primary key unique, class text, token text unique, registered bool, email_sent bool, day text)'
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



@tasks.loop(seconds=10)
async def sync_db():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/gmail.send']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1-JEKV1K6EUsjD_ySjdOiAfw0P5Do3_no56xzcgLT9n8'
    SAMPLE_RANGE_NAME = 'B2:K500'
    invite_link = "https://discord.gg/dkQdAeEH"


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

        # sync google sheets with db
        else:
            print("Syncing with db....")
            print(f'Inserting {len(values)} records')
            for row in values:
                # Add members into db
                cursor.execute('''INSERT OR IGNORE INTO members(
                   name,email,id,class,token,registered,email_sent, day) VALUES 
                   (?,?,?,?,?,?,?)''',(row[0],row[1],int(row[2]),row[5],str(uuid.uuid4()),0,0,row[6]) ) 
                connection.commit()

    except HttpError as err:
        print(err)

    # search for the member who didn't receive an invitation yet
    rows = cursor.execute("SELECT * FROM members WHERE email_sent= FALSE").fetchall()
    for row in rows:
        try:
            service = build('gmail', 'v1', credentials=creds)
            message = MIMEMultipart()

            html = f"""\
        <!doctype html>
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

        <head>
            <title>

            </title>
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
             <!-- <meta http-equiv="refresh" content="5" /> -->
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style type="text/css">
                #outlook a {{
                    padding: 0;
                }}

                .ReadMsgBody {{
                    width: 100%;
                }}

                .ExternalClass {{
                    width: 100%;
                }}

                .ExternalClass * {{
                    line-height: 100%;
                }}

                body {{
                    margin: 0;
                    padding: 0;
                    -webkit-text-size-adjust: 100%;
                    -ms-text-size-adjust: 100%;
                }}

                table,
                td {{
                    border-collapse: collapse;
                    mso-table-lspace: 0pt;
                    mso-table-rspace: 0pt;
                }}

                img {{
                    border: 0;
                    height: auto;
                    line-height: 100%;
                    outline: none;
                    text-decoration: none;
                    -ms-interpolation-mode: bicubic;
                }}

                p {{
                    display: block;
                    margin: 13px 0;
                }}
            </style>

            <style type="text/css">
                @media only screen and (max-width:480px) {{
                    @-ms-viewport {{
                        width: 320px;
                    }}
                    @viewport {{
                        width: 320px;
                    }}
                }}
            </style>


            <style type="text/css">
                @media only screen and (min-width:480px) {{
                    .mj-column-per-100 {{
                        width: 100% !important;
                    }}
                }}
            </style>


            <style type="text/css">
            </style>

        </head>

        <body style="background-color:#f9f9f9;">


            <div style="background-color:#f9f9f9;">




                <div style="background:#f9f9f9;background-color:#f9f9f9;Margin:0px auto;max-width:600px;">

                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#f9f9f9;background-color:#f9f9f9;width:100%;">
                        <tbody>
                            <tr>
                                <td style="border-bottom:#333957 solid 5px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">

                                </td>
                            </tr>
                        </tbody>
                    </table>

                </div>





                <div style="background:#fff;background-color:#fff;Margin:0px auto;max-width:600px;">

                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%;">
                        <tbody>
                            <tr>
                                <td style="border:#dddddd solid 1px;border-top:0px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">

                                    <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:bottom;" width="100%">

                                            <tr>
                                                <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                                        <tbody>
                                                            <tr>
                                                                <td style="width:64px;">

                                                                    <img height="auto" src="https://ci3.googleusercontent.com/mail-sig/AIorK4yKLsdY17j_7YURkbXBcR5vmOzQmfyodgKA_BrkgCm0UDtIa_MwiYgao-bPooRYJTGTTly4_Rw" style="border:0;display:block;outline:none;text-decoration:none;width:200%;" width="64" />

                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>

                                            <tr>
                                                <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:40px;word-break:break-word;">

                                                    <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:28px;font-weight:bold;line-height:1;text-align:center;color:#555;">
                                                        Welcome to the Cyber Security Club
                                                    </div>

                                                </td>
                                            </tr>

                                            <tr>
                                                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                                    <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;">
                                                        Hello { row[0] } and welcome, please follow the steps below to join the club's discord server:<br><br>1 - Go to <a href="https://discord.com">https://discord.com</a>  (Skip this if you have discord already!)<br><br>2 - Download Discord (Windows, Linux, MacOS, Android, IOS).<br><br>3 - Create an account.<br><br>4 - Open the following link to join the server: <a href="{ invite_link }">{ invite_link }</a><br><br>5 - Our Discord bot will send you a DM.<br><br>6 - Reply to the DM with the following command to be able to access your training channels:
                                                        <br><br>
                                                        <code style="background-color: #f1f1f1; padding: 5px; border-radius: 7px;">&nbsp;&nbsp;!verify { row[2] } { row[4] }&nbsp;&nbsp;</code>
                                                        <br><br>7 - Class Details: {row[5]}
                                                        <br><br>
                                                    </div>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:20px;padding-bottom:10px;word-break:break-word;">

                                                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                                                        <tr>
                                                            <td align="center" bgcolor="#2F67F6" role="presentation" style="border:none;border-radius:6px;color:#ffffff;cursor:auto;padding:15px 25px;" valign="middle">
                                                                <a href="https://discord.com" style="background:#2F67F6;color:#ffffff;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;font-weight:normal;line-height:120%;Margin:0;text-decoration:none;text-transform:none;">
                                                                    Join our Discord!
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>

                                                </td>
                                            </tr>

                                            <tr>
                                                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                                    <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:14px;line-height:20px;text-align:left;color:#525252;">
                                                        Best regards,<br> Cyber Security Club<br>PSUT<br>
                                                        <a href="https://cscpsut.com" style="color:#2F67F6">cscpsut.com</a>
                                                    </div>

                                                </td>
                                            </tr>

                                        </table>

                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style="Margin:0px auto;max-width:600px;">

                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                        <tbody>
                            <tr>
                                <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">


                                    <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td style="vertical-align:bottom;padding:0;">

                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">

                                                            

                                                        </table>

                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>

                                    </div>   
                                </td>
                            </tr>
                        </tbody>
                    </table>

                </div>

            </div>

        </body>

        </html>
            """

            message['To'] = row[1]
            message['From'] = 'omar2001.oh@gmail.com'
            message['Subject'] = 'Join our Discord!'
            message.attach(MIMEText(html, "html"))


            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()


            create_message = {
                'raw': encoded_message
            }

            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())

            # set email_sent to TRUE to avoid sending again
            cursor.execute(
                "UPDATE members SET email_sent = TRUE WHERE id = ?",
                (row[2],)
            )
            connection.commit()
            
            # throttling just in case
            time.sleep(0.001)

        except HttpError as error:
            print(F'An error occurred: {error}')





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
    
    if token != rows[0][4]:   # Check if token is invalid
        await ctx.send(f'Invalid Token, make sure that your Token is correct')
        return
    
    if rows[0][5]:  # Check if user has registered previously
        await ctx.send(f'Token and ID pair have already been used.')
        return
    
    name = rows[0][0]
    level = rows[0][3]
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


    time.sleep(2)   # doing all these checks is tiring so I need to rest hahaha

    # set registered to TRUE to avoid token reuse
    cursor.execute(
        "UPDATE members SET registered = TRUE WHERE id = ?",
        (ID,)
    )
    connection.commit()

    ctr = 0
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