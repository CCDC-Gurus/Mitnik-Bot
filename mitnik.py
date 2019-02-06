## Mitnik - CCDC Discord Helper
## A bot to provide help with different CCDC functions such as
## incident reports, inject monitoring, and password generation.
## Gavin Lewis - 2018

"""

    Imports

    
"""

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging
import os
import urllib.request
import requests
import shutil

import IncidentWriter
import PasswdGen
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
    - Incident Creator
        a) Manage and create incident reports
    - Password generator

"""

"""
    Logging functions
"""

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = """You better work"""

## Make sure directories are there
if not(os.path.isdir("images")):
    os.mkdir("images")
if not(os.path.isdir("inc_tex")):
    os.mkdir("inc_tex")
if not(os.path.isdir("inc_raw")):
    os.mkdir("inc_raw")


## Init the bot
client = commands.Bot(command_prefix = "?", description=description)

"""
    Tools
"""

def tool_countIncidents():
    count = 0
    for name in os.listdir('./inc_raw'):
        count += 1
    return count

# Runs on turn on
@client.event
async def on_ready():
    print("Mitnik: ONLINE")
    
    print("Current incidents: " + str(tool_countIncidents()))
    
## Commands
HELP = '?HELP'
INC_EDIT = '?INCIDENT -e '

@client.command()
async def add(ctx,arg):
    print("HERE:")
    await ctx.send(arg)

# Reactions to messages
@client.event
async def on_message(message):
    HELP_MSG = """Welcome, I am Mitnik, here to help you.
    (Use the flag -H on any command to find help)
    
?HELP - Bring up this message
?INCIDENT - Create/Edit/List Incidents
?GENPASS - Generate a password"""
    
    INCIDENT_MSG = """Choose a flag:
-e [num]             edit incident [num]
-l [num]             lists current incidents (or a single incident)
-n                   create a new incident"""

    INCIDENT_TAGS = ["Number", "Img Path", "Attacker", "Target", "Found", "Vulnerability", "Response Taken", "Result"]

    ## Debug stuff
    auth = str(message.author)
    print(auth + ": " + message.content) # Print to console
    msg = str(message.content.upper())
    
    ## TEST ZONE
    #print(len(message.embeds))
    #print(message.attachments[0])
    #if (len(message.embeds) > 0):
    #    print(message.embeds[0].title)
    #    print(message.embeds[0].type)
    #    print(message.embeds[0].url)
    #    print(message.embeds[0].image)
    
    
    
    
        
    ## Command switch
    if msg.startswith('?'):
        args = msg.split(" ")

################################################################################################
        if args[0] == '?HELP':
            
            if (len(args) == 1):
                await client.send_message(message.channel, HELP_MSG)
            elif (len(args) > 1):
                await client.send_message(message.channel, "Not implemented yet")
                
################################################################################################        
        if args[0] == '?INCIDENT':

            ## There is only one argument
            if (len(args) == 1):
                await client.send_message(message.channel, INCIDENT_MSG)
                        
            ## THERE IS exactly 2 ARGUMENTS    
            elif (len(args) == 2): 
            
                if (args[1] == '-H'):
                    await client.send_message(message.channel, INCIDENT_MSG)
                    
                ## 2ARG - NEW MODE
                elif (args[1] == '-N'):
                    # Create new incident
                    incident = IncidentWriter.Incident(tool_countIncidents()+1)
                    
                    
                    # IMAGES - Send message
                    await client.send_message(message.channel, 'New Incident #' + str(incident.get_num()) + "\nBe as detailed as possible.\n")
                    await client.send_message(message.channel, 'Upload all relevant images:\n(Type "done" when finished.)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    
                    num_imgs = 1 # For naming the images
                    img_names = [] # To save correctly
                    
                    while (len(input.attachments) > 0): # Incase they somehow attach two images to the same message, may not work though
                        print(input.attachments[0]["url"])
                        
                        # Have to send a different user-agent to get the pics
                        r = requests.get(input.attachments[0]["url"], stream=True, headers={'User-agent': 'Mozilla/5.0'})
                        name = "inc_" + str(tool_countIncidents()+1) + "_img_" + str(num_imgs) + ".jpg"
                        img_names.append(name)
                        if r.status_code == 200:
                            with open(name, 'wb') as f:
                                r.raw.decode_content = True
                                shutil.copyfileobj(r.raw, f)
                        else:
                            print("Failed to grab image")
                            await client.send_message(message.channel, 'Did not grab that last image. Try again.')
    
                        input = await client.wait_for_message(author=message.author)
                        num_imgs += 1

                    # Set images
                    incident.set_imgs(img_names)
                    
                    # ATTACKER - Send message
                    await client.send_message(message.channel,'Who attacked the box?:\n(n/a if unknown.)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set attacker
                    incident.set_attacker(input.content)
                    
                    # TARGET - Send message
                    await client.send_message(message.channel,'Enter Target info:\n(What box/system/process was attacked)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set attacker
                    incident.set_target(input.content)
                    
                    # FOUND - Send message
                    await client.send_message(message.channel,'Enter how incident was Found:\n(Logs, searching dir, rkhunter)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set attacker
                    incident.set_found(input.content)
                    
                    # VULN - Send message
                    await client.send_message(message.channel,'Enter what was Vulnerable:\n(Might be inherent in the box/process)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set vulnerability
                    incident.set_vulnerability(input.content)
                    
                    # RESPONSE - Send message
                    await client.send_message(message.channel,'Enter Response taken:\n(This can be kicking a user, deleting a file, blocking IP, etc)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set response
                    incident.set_response(input.content)
                    
                    # RESULT - Send message
                    await client.send_message(message.channel,'Enter Result of Repsonse:\n(Are they gone, was data stolen)')
                    # Receive input
                    input = await client.wait_for_message(author=message.author)
                    # Set result
                    incident.set_result(input.content)
                    
                    ## All saves were successful
                    if (incident.saveall()):
                        await client.send_message(message.channel,'Saving was successful.')
                    else:
                        await client.send_message(message.channel,'Something went wrong, yell at someone.')
                    
                    
                # 2ARG - LIST MODE
                elif (args[1] == '-L'):
                    output = ""
                    cnt = 1
                    if tool_countIncidents() > 0:
                        for fin in os.listdir("./inc_raw/"):  # For each file

                            output += "Incident num " + str(cnt) + ":\n"
                            with open(os.path.join("./inc_raw/",fin),"r") as file:
                                i = 0
                                for line in file:
                                    output += INCIDENT_TAGS[i] + "> " + str(line) + "\n"
                                    i += 1
                            output += "\n"
                            cnt += 1
                    else:
                        output = "No valid incidents yet."

                    await client.send_message(message.channel,output)    
                    
                # 2ARG - INVALID FLAG
                else:
                    # Send error
                    if (args[1] == '-E'):
                        await client.send_message(message.channel, 'Invalid incident number')
                    else:
                        await client.send_message(message.channel, 'Invalid flag')
                        func_help(message,client)
        
            
            ## There is exactly 3 arguments
            elif (len(args) == 3):
                
                ## 3ARG - EDIT MODE
                if (args[1] == '-E'):
                    # Check this is a valid edit
                    inc_2_edit = int(args[2])
                    if (inc_2_edit > 0 and inc_2_edit <= tool_countIncidents()):
                        
                        # Choose parts to edit
                        MENU = """Which would you like to edit (seperate multiple choices with commas):
                        1) Image Paths
                        2) Attacker Info
                        3) Target Info
                        4) Vulnerability
                        5) Response Taken
                        6) Results\n"""
                        
                        # Obtain a valid option to choose
                        ready = False
                        while not ready:
                            # Send message
                            await client.send_message(message.channel, MENU)
                            # Receive message
                            input = await client.wait_for_message(author=message.author)
                            
                            ready = True
                            input = input.content.split(',')
                            if len(input) < 1: # If blank
                                ready = False # Get new data
                            else:
                                for i in range(len(input)):
                                    input[i] = int(input[i])
                                    if (input[i] < 1 or input[i] > 6): # Make sure valid
                                        await client.send_message(message.channel, "Invalid option: " + str(input[i]) + ", choose again")
                                        ready = False
                                            
                        # Pull up the incident
                        incident = IncidentWriter.Incident(inc_2_edit)
                        incident.fromexisting(inc_2_edit)
                        
                        # Edit each part listed
                        for attr in input:
                            
                            if attr == 1:
                                await client.send_message(message.channel, 'Update path to images:')
                                # Receive input
                                input = await client.wait_for_message(author=message.author)
                                # Set images
                                incident.set_imgs("test")
                            elif attr == 2:
                                # Send message
                                await client.send_message(message.channel,'Update Attacker info:')
                                # Receive input
                                input = await client.wait_for_message(author=message.author)
                                # Set attacker
                                incident.set_attacker(input.content)
                            elif attr == 3:
                                # Send message
                                await client.send_message(message.channel,'Update Target info:')
                                # Receive input
                                input = await client.wait_for_message(author=message.author)
                                # Set attacker
                                incident.set_target(input.content)
                            elif attr == 4:
                                # Send message
                                await client.send_message(message.channel,'Update what was Vulnerable:')
                                # Receive input
                                input = await client.wait_for_message(author=message.author)
                                # Set vulnerability
                                incident.set_vulnerability(input.content)
                            elif attr == 5:
                                # Send message
                                await client.send_message(message.channel,'Update Response taken:')
                                # Receive input
                                input = await client.wait_for_message(author=message.author)
                                # Set response
                                incident.set_response(input.content)
                            elif attr == 6:
                                # Send message
                                await client.send_message(message.channel,'Update Result of Repsonse:')
                                # Receive input
                                input = await client.wait_for_message(author=message.author)
                                # Set result
                                incident.set_result(input.content)
                                
                        incident.saveall()

                    else:
                        print("Invalied incident target")
                
                # 3ARG - LIST MODE
                elif (args[1] == '-L'):
                    output = ""
                    TOT_INC = tool_countIncidents()
                    inc2edit = int(args[2])
                    
                    # If valid
                    if inc2edit > 0 and inc2edit <= TOT_INC:
                        output += "Incident num " + str(inc2edit) + ":\n"
                        with open(os.path.join("./inc_raw/",str(inc2edit)+".txt"),"r") as file:
                            i = 0
                            for line in file:
                                output += INCIDENT_TAGS[i] + "> " + str(line) + "\n"
                                i += 1
                            output += "\n"
                    else:
                        output = "Not a valid incident to edit."

                    await client.send_message(message.channel,output)
                else:
                    # Send error
                    await client.send_message(message.channel, 'Invalid incident chosen.')
            
################################################################################################
        if args[0] == '?GENPASS':
            
            if (len(args) == 1):
                passwd = PasswdGen.gen_password()
                await client.send_message(message.channel, "New password: " + passwd)
            
            elif (len(args) == 2):
                if (int(args[1]) > 6):
                    await client.send_message(message.channel, "That might be too long, keep it 5 or less")
                elif (int(args[1]) > 0):
                    passwd = PasswdGen.gen_password(int(args[1]))
                    await client.send_message(message.channel, "New password: " + passwd)
                elif (args[1] == "-H"):
                    await client.send_message(message.channel, "?GENPASS [0 < num <= 5]\n  Will generate a password of the length provided.")
                else:
                    await client.send_message(message.channel, "Invalid use of this command.")
                

   
    
    
    
## Connect to discord and come online
client.run(secrets.TOKEN)
