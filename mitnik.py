import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging
import os

import IncidentWriter
import secrets

## Have to run this
## https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=0
## to add to a server. Need manage permissions

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

## Logging functions
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = """You better work"""
## Init the bot
#Client = discord.Client()
client = commands.Bot(command_prefix = "?", description=description)

def tool_countIncidents():
    return len([name for name in os.listdir('./Incidents') if os.path.isfile(name)])





# Runs on turn on
@client.event
async def on_ready():
    print("Mitnik: ONLINE")
    
    print("Current incidents: " + str(tool_countIncidents()))
    
    
HELP_MSG = """This is where help stuff would be, if there was any written"""
INCIDENT_MSG = """Choose a flag:
-e [num]             edit incident [num]
-l                   lists current incidents
-n [num] <>Data<>    create a new incident"""

## Commands
HELP = '?HELP'
INC_EDIT = '?INCIDENT -e '



incident_list = []
tot_incidents = tool_countIncidents()


@client.command()
async def add(ctx,arg):
    print("HERE:")
    await ctx.send(arg)

# Reactions to messages
@client.event
async def on_message(message):

    auth = str(message.author)
    msg = str(message.content.upper())
        
    print(auth + ": " + msg)
    
    #if msg.startswith('?HELP'):
    #    args = message.content.split(" ")
    #    if (len(args) == 1):
    #        await client.send_message(message.channel, HELP_MSG)
    #    elif (len(args) > 1):
    #        await client.send   _message(message.channel, "Not implemented yet")
            
    if msg.startswith('?'):
        args = msg.split(" ")
        
        if args[0] == '?HELP':
            if (len(args) == 1):
                await client.send_message(message.channel, HELP_MSG)
            elif (len(args) > 1):
                await client.send_message(message.channel, "Not implemented yet")
        
        if args[0] == '?INCIDENT':
            ## There is only one argument
            if (len(args) == 1):
                await client.send_message(message.channel, "Here will be a list of the flags.")
               
            ## There is exactly 3 arguments
            elif (len(args) == 3):
                
                ## EDIT MODE
                if (args[1] == '-E'):
                    # Check this is a valid edit
                    inc_2_edit = int(args[2])
                    if (args[inc_2_edit] > 0 and args[inc_2_edit] <= tot_incidents):
                        MENU = """Which would you like to edit:
                        1) Image Paths
                        2) Attacker Info
                        3) Target Info
                        4) Vulnerability
                        5) Response Taken
                        6) Results\n"""
                        
                        # Send message
                        await client.send_message(message.channel, MENU)
                        
                        
                        
                        
                        
                else:
                    # Send error
                    await client.send_message(message.channel, 'Invalid flag')
                        
                        
                        
                        
                
            elif (len(args) == 2):  
                ## NEW MODE
                if (args[1] == '-N'):
                    # Create new incident
                    incident_list.append(IncidentWriter.Incident(tot_incidents+1))

                    # Send message
                    await client.send_message(message.channel, 'New Incident #' + str(tot_incidents+1))
                    await client.send_message(message.channel, 'Enter path to images:')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set images
                    incident_list[-1].set_imgs("test")
                    
                    # Send message
                    await client.send_message(message.channel,'Enter Attacker info:')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set attacker
                    incident_list[-1].set_attacker(input)
                    
                    # Send message
                    await client.send_message(message.channel,'Enter Target info:')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set attacker
                    incident_list[-1].set_target(input)
                    
                    # Send message
                    await client.send_message(message.channel,'Enter what was Vulnerable:')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set vulnerability
                    incident_list[-1].set_vulnerability(input)
                    
                    # Send message
                    await client.send_message(message.channel,'Enter Response taken:')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set response
                    incident_list[-1].set_response(input)
                    
                    # Send message
                    await client.send_message(message.channel,'Enter Result of Repsonse:')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set result
                    incident_list[-1].set_result(input)
                    
                    
                    
                    
                    
                    
                    
                    
                
                




                else:
                    # Send error
                    await client.send_message(message.channel, 'Invalid flag')
            
            
            
            
            
            elif (args[1] == '-n'):    
                pass
            elif (args[1] == '-l'):    
                pass
    
            
    #if msg.startswith(INC_EDIT):
    #    last_ind = msg.index(" ",len(INC_EDIT))
    #    inc_num = int(msg[len(INC_EDIT):msg.index(" ",len(INC_EDIT))])
    #    if inc_num < 1:
    #        await client.send_message(message.channel, "Incident number must be one or greater.")
    #    if inc_num in incident_list.keys():
    #        data = msg[last_ind+1:]
    #        print(inc_num, data)
    #    else:
    #        await client.send_message(message.channel, "Not a valid incident.")
        
        
    
    
    
## Connect to discord and come online
client.run(secrets.TOKEN)
