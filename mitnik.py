import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging

import secrets

## Have to run this
## https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=0
## to add to a server. Need manage permissions

## Logging functions
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

## Init the bot
Client = discord.Client()
client = commands.Bot(command_prefix = "?")

"""

This bot will have a few functions

    - Timer for injects
        a) Display description
        b) Display who is on it, so assign people
        c) Timer reminders
    - Show who is in charge of which box
        a) Return who is on it
        b) Return IP, function, other relevant data
    - Return important bits of code?
        a) Maybe if a github is setup this will return stuff and be legal
    
        

"""

# Runs on turn on
@client.event
async def on_ready():
    print("Mitnik: ONLINE")
    
    
HELP_MSG = """This is where help stuff would be, if there was any written"""

# Reactions to messages
@client.event
async def on_message(message):

    auth = str(message.author)
    msg = str(message.content.upper())
        
    print(auth + ": " + msg)
    
    if msg.startswith('?HELP'):
        args = message.content.split(" ")
        if (len(args) == 1):
            await client.send_message(message.channel, HELP_MSG)
        elif (len(args) > 1):
            await client.send_message(message.channel, "Not implemented yet")
    
    
    
## Connect to discord and come online
client.run(secrets.TOKEN)
