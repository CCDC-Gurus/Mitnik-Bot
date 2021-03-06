#Tested on these version
#Discord.py - 1.3.1
#aiohttp - 3.6.2
# Mitnik - CCDC Discord Helper
# A bot to provide help with different CCDC functions such as
# incident reports, inject monitoring, and password generation.
# Gavin Lewis - 2018
from discord.ext import commands
import logging
import os
import requests
import shutil
import random

import IncidentWriter
import PasswdGen
from config import configs
# Have to run this
# https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=0
# to add to a server. Need manage permissions

"""This bot will have a few functions

    - Timer for injects
        a) Display description          
        b) Display who is on it, so assign people
        c) Timer reminders
    - Incident Creator
        a) Manage and create incident reports
    - Password generator
"""

# Logging functions
log = False
if log:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)



# Make sure directories are there
if not(os.path.isdir("images")):
    os.mkdir("images")
if not(os.path.isdir("inc_tex")):
    os.mkdir("inc_tex")
if not(os.path.isdir("inc_raw")):
    os.mkdir("inc_raw")


# Init the bot
client = commands.Bot(command_prefix=configs["prefix"], description=configs["desc"])

# Tools
def tool_countIncidents():
    count = 0
    for name in os.listdir('./inc_raw'):
        count += 1
    return count

    
# Runs on turn on
@client.event
async def on_ready():
    """Run on bot start"""
    print("Mitnik: ONLINE")
    
    print("Current incidents: " + str(tool_countIncidents()))


@client.command()
async def add(ctx, arg):
    """Not sure what this was for."""

    print("HERE:")
    await ctx.send(arg)


# Reactions to messages
@client.event
async def on_message(message):
    """Handles and reacts to messages."""

    HELP_MSG = """Welcome, I am Mitnik, here to help you.
    (Use the flag -H on any command to find help)
    
!HELP - Bring up this message
!INCIDENT - Create/Edit/List Incidents
!GENPASS - Generate a password
!SANDWICH - Hungry?"""
    
    INCIDENT_MSG = """Choose a flag:
-e [num]             edit incident [num]
-l [num]             lists current incidents (or a single incident)
-n                   create a new incident"""

    INCIDENT_TAGS = ["Number", "Img Path", "Attacker", "Target", "Found", "Vulnerability", "Response Taken", "Result"]

    # Debug stuff
    auth = str(message.author) # Author of this message
    curr_channel = message.channel # Channel this message is from
    print(auth + ": " + message.content) # Print to console
    msg = str(message.content.upper())

    # Command switch
    if msg.startswith('!'):
        args = msg.split(" ")

        if args[0] == '!HELP':
            
            if len(args) == 1:
                await message.channel.send(HELP_MSG)
            elif len(args) > 1:
                await message.channel.send("Not implemented yet")

        if args[0] == '!INCIDENT':

            ######################################################
            #
            #     INCIDENT - 1 Argument - List all flags
            #
            ######################################################
            if len(args) == 1:
                await message.channel.send(INCIDENT_MSG)

            ######################################################
            #
            #     INCIDENT - 2 Arguments - HELP - NEW - LIST - INVALID
            #
            ######################################################
            elif len(args) == 2:

                # 2ARG - HELP MODE
                if args[1] == '-H':
                    await message.channel.send(INCIDENT_MSG)

                # 2ARG - NEW MODE
                elif args[1] == '-N':
                    # Create new incident
                    incident = IncidentWriter.Incident(tool_countIncidents()+1)

                    # IMAGES - Send message
                    await message.channel.send(
                                              'New Incident #' + str(incident.get_num())
                                              + "\nBe as detailed as possible.\n")
                    await message.channel.send(
                                              'Upload all relevant images:\n(Type "done" when finished.)')
                    
                    # Receive input
                    def pred(m):
                        return m.author == message.author and m.channel == message.channel
                    input = await client.wait_for('message',check=pred)
                    
                    num_imgs = 1  # For naming the images
                    img_names = []  # To save correctly

                    # In case they somehow attach two images to the same message, may not work though
                    while len(input.attachments) > 0:
                        print(input.attachments[0]["url"])
                        
                        # Have to send a different user-agent to get the pics
                        r = requests.get(input.attachments[0]["url"], stream=True, headers={'User-agent': 'Mozilla/5.0'})
                        name = "inc_" + str(tool_countIncidents()+1) + "_img_" + str(num_imgs) + ".jpg"
                        img_names.append(name)
                        if r.status_code == 200:
                            with open("images\\" + name, 'wb') as f:
                                r.raw.decode_content = True
                                shutil.copyfileobj(r.raw, f)
                        else:
                            print("Failed to grab image")
                            await message.channel.send('Did not grab that last image. Try again.')
    
                        input = await client.wait_for('message',check=pred)
                        num_imgs += 1

                    # Set images
                    incident.set_imgs(img_names)
                    
                    # ATTACKER - Send message
                    await message.channel.send('Who attacked the box?:\n(n/a if unknown.)')
                    # Receive input
                    input = await client.wait_for('message',check=pred)
                    # Set attacker
                    incident.set_attacker(input.content)
                    
                    # TARGET - Send message
                    await message.channel.send('Enter Target info:\n(What box/system/process was attacked)')
                    # Receive input
                    input = await client.wait_for('message',check=pred)
                    # Set attacker
                    incident.set_target(input.content)
                    
                    # FOUND - Send message
                    await message.channel.send('Enter how incident was Found:\n(Logs, searching dir, rkhunter)')
                    # Receive input
                    input = await client.wait_for('message',check=pred)
                    # Set attacker
                    incident.set_found(input.content)
                    
                    # VULN - Send message
                    await message.channel.send('Enter what was Vulnerable:\n(Might be inherent in the box/process)')
                    # Receive input
                    input = await client.wait_for('message',check=pred)
                    # Set vulnerability
                    incident.set_vulnerability(input.content)
                    
                    # RESPONSE - Send message
                    await message.channel.send('Enter Response taken:'
                                              '\n(This can be kicking a user, deleting a file, blocking IP, etc)')
                    # Receive input
                    input = await client.wait_for('message',check=pred)
                    # Set response
                    incident.set_response(input.content)
                    
                    # RESULT - Send message
                    await message.channel.send('Enter Result of Response:\n(Are they gone, was data stolen)')
                    # Receive input
                    input = await client.wait_for('message',check=pred)
                    # Set result
                    incident.set_result(input.content)
                    
                    # All saves were successful
                    if incident.saveall():
                        await message.channel.send('Saving was successful.')
                    else:
                        await message.channel.send('Something went wrong, yell at someone.')

                # 2ARG - LIST MODE
                elif args[1] == '-L':
                    output = ""
                    cnt = 1
                    if tool_countIncidents() > 0:
                        for fin in os.listdir("./inc_raw/"):  # For each file

                            output += "Incident num " + str(cnt) + ":\n"
                            with open(os.path.join("./inc_raw/", fin), "r") as file:
                                i = 0
                                for line in file:
                                    output += INCIDENT_TAGS[i] + "> " + str(line) + "\n"
                                    i += 1
                            output += "\n"
                            cnt += 1
                    else:
                        output = "No valid incidents yet."

                    await message.channel.send(output)    
                    
                # 2ARG - INVALID FLAG
                else:
                    # Send error
                    if args[1] == '-E':
                        await message.channel.send('Invalid incident number')
                    else:
                        await message.channel.send('Invalid flag')
                        #func_help(message, client)

            ######################################################
            #
            #     INCIDENT - 3 Arguments - EDIT - LIST - INVALID
            #
            ######################################################
            elif (len(args) == 3):
                
                # 3ARG - EDIT MODE
                if args[1] == '-E':
                    # Check this is a valid edit
                    inc_2_edit = int(args[2])
                    if 0 < inc_2_edit <= tool_countIncidents():
                        
                        # Choose parts to edit
                        MENU = """Which would you like to edit (seperate multiple choices with commas):
                        1) Image Paths
                        2) Attacker Info
                        3) Target Info
                        4) How incident was found
                        5) Vulnerability
                        6) Response Taken
                        7) Results\n"""
                        
                        # Obtain a valid option to choose
                        ready = False
                        while not ready:
                            # Send message
                            await message.channel.send(MENU)
                            # Receive message
                            input = await client.wait_for('message',check=pred)
                            
                            ready = True
                            input = input.content.split(',')
                            if len(input) < 1: # If blank
                                ready = False # Get new data
                            else:
                                for i in range(len(input)):
                                    input[i] = int(input[i])
                                    if (input[i] < 1 or input[i] > 6): # Make sure valid
                                        await message.channel.send("Invalid option: " + str(input[i]) + ", choose again")
                                        ready = False
                                            
                        # Pull up the incident
                        incident = IncidentWriter.Incident(inc_2_edit)
                        incident.fromexisting(inc_2_edit)
                        
                        # Edit each part listed
                        for attr in input:
                            
                            if attr == 1:
                                await message.channel.send('Update path to images:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set images
                                incident.set_imgs("test")
                            elif attr == 2:
                                # Send message
                                await message.channel.send('Update Attacker info:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set attacker
                                incident.set_attacker(input.content)
                            elif attr == 3:
                                # Send message
                                await message.channel.send('Update Target info:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set attacker
                                incident.set_target(input.content)
                            elif attr == 4:    
                                # Send message
                                await message.channel.send('Update how the incident was found:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set vulnerability
                                incident.set_found(input.content)
                            elif attr == 5:
                                # Send message
                                await message.channel.send('Update what was Vulnerable:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set vulnerability
                                incident.set_vulnerability(input.content)
                            elif attr == 6:
                                # Send message
                                await message.channel.send('Update Response taken:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set response
                                incident.set_response(input.content)
                            elif attr == 7:
                                # Send message
                                await message.channel.send('Update Result of Response:')
                                # Receive input
                                input = await client.wait_for('message',check=pred)
                                # Set result
                                incident.set_result(input.content)
                                
                        incident.saveall()

                    else:
                        print("Invalid incident target")
                
                # 3ARG - LIST MODE
                elif args[1] == '-L':
                    output = ""
                    TOT_INC = tool_countIncidents()
                    inc2edit = int(args[2])
                    
                    # If valid
                    if 0 < inc2edit <= TOT_INC:
                        output += "Incident num " + str(inc2edit) + ":\n"
                        with open(os.path.join("./inc_raw/", str(inc2edit)+".txt"), "r") as file:
                            i = 0
                            for line in file:
                                output += INCIDENT_TAGS[i] + "> " + str(line) + "\n"
                                i += 1
                            output += "\n"
                    else:
                        output = "Not a valid incident to edit."

                    await message.channel.send(output)

                # 3ARG - INVALID FLAG
                else:
                    # Send error
                    await message.channel.send('Invalid flag usage.')
            
################################################################################################
################################################################################################
        if args[0] == '!GENPASS':
            
            if len(args) == 1:
                passwd = PasswdGen.gen_password()
                await message.channel.send("New password: " + passwd)
            
            elif len(args) == 2:
                if int(args[1]) > 6:
                    await message.channel.send("That might be too long, keep it 5 or less")
                elif int(args[1]) > 0:
                    passwd = PasswdGen.gen_password(int(args[1]))
                    await message.channel.send("New password: " + passwd)
                elif args[1] == "-H":
                    await message.channel.send("?GENPASS [0 < num <= 5]"
                                              "\n  Will generate a password of the length provided.")
                else:
                    await message.channel.send("Invalid use of this command.")

################################################################################################
################################################################################################
        if args[0] == '!SANDWICH':
            num = random.randint(0,6)
            with open('sandwich\\' + str(num) + '.jpg', 'rb') as f:
                await message.channel.send(f)

# Connect to discord and come online
client.run(configs["secret"])