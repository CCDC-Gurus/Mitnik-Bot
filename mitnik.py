#Tested on these version
#Discord.py - 1.3.1
#aiohttp - 3.6.2
# Mitnik - CCDC Discord Helper
# A bot to provide help with different CCDC functions such as
# incident reports, inject monitoring, and password generation.
# Gavin Lewis - 2018
import discord
from discord.ext import commands
import logging
import os
import requests
import shutil
import threading
import random
import re

import DBManager as dbm
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
# if not(os.path.isdir("data")):
#     os.mkdir("data")

# Create general info table
dbm.create_general()

# Init the bot
client = commands.Bot(command_prefix=configs["prefix"], description=configs["desc"])

# Tools
def tool_countIncidents():
    count = 0
    for name in os.listdir('./inc_raw'):
        count += 1
    return count

def injectChecker():
    """Check the inject db, alert team when """
    pass

def re_validEventName(name):
    """Checks if event name is valid for sys"""
    if len(name) > 255:
        return False
    return re.search("^[A-Za-z0-9-]+$", name)

def re_validFirstName(name):
    """Checks if first name is valid"""
    if len(name) > 255:
        return False
    return re.search("[A-Za-z-]+", name)

# Runs on turn on
@client.event
async def on_ready():
    """Run on bot start"""
    print("Mitnik: ONLINE")
    
    print("Current incidents: " + str(tool_countIncidents()))

    # Need to start the Inject time checker
    #inject_thread = threading.Thread(target=thread_function, args=(1,), daemon=True)


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

    EVENT_MSG = """Choose a flag:
-n [name]          create new event [name]. Use only letters, numbers and hyphens.
-l                 list all events and their status
-r [name]          resume an event [name]
-c                 show current event
-j [first-name]    Join the active event. Use only letters and hyphens.
-d [name]          Delete the event [name]"""

    # Debug stuff
    auth = str(message.author) # Author of this message
    curr_channel = message.channel # Channel this message is from
    print(auth + ": " + message.content) # Print to console
    msg = str(message.content.upper())

    def pred(m):
        return m.author == message.author and m.channel == message.channel

    # Command switch
    if msg.startswith('!'):
        args = msg.split(" ")

        if args[0] == '!HELP':
            
            if len(args) == 1:
                await message.channel.send(HELP_MSG)
            elif len(args) > 1:
                await message.channel.send("Not implemented yet")

################################################################################################
################################################################################################
        if args[0] == '!INCIDENT':
            try:
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
                                input = await client.wait_for('message', check=pred)
                                
                                ready = True
                                input = input.content.split(',')
                                if len(input) < 1: # If blank
                                    ready = False # Get new data
                                else:
                                    for i in range(len(input)):
                                        input[i] = int(input[i])
                                        if (input[i] < 1 or input[i] > 8): # Make sure valid
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
                                    
                            # Overwrite both the txt and tex files
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
            except Exception as e:
                print(e)
                await message.channel.send('Something went wrong, yell at the captain (logs in terminal)')
            
################################################################################################
################################################################################################
        if args[0] == '!GENPASS':
            
            if len(args) == 1:
                passwd = PasswdGen.gen_password()
                await message.channel.send("New password: " + passwd)
            
            elif len(args) == 2:
                try:
                    if args[1] == "-H":
                        await message.channel.send("?GENPASS [0 < num <= 5]"
                                                "\n  Will generate a password of the length provided.")
                    elif int(args[1]) > 6:
                        await message.channel.send("That might be too long, keep it 5 or less")
                    elif int(args[1]) > 0:
                        passwd = PasswdGen.gen_password(int(args[1]))
                        await message.channel.send("New password: " + passwd)    
                    else:
                        await message.channel.send("Invalid use of this command.")
                except:
                    await message.channel.send("Something went wrong, try checking your syntax")

################################################################################################
################################################################################################
        if args[0] == '!SANDWICH':
            num = random.randint(1,5)
            await message.channel.send(file=discord.File(os.path.join("sandwich", str(num) + ".jpg")))

################################################################################################
################################################################################################
        if args[0] == '!EVENT':
            
            if len(args) == 1:
                # Send the EVENT help message
                await message.channel.send(EVENT_MSG)

            elif len(args) == 2:
                if args[1] == '-L':
                    """ List events """
                    event_list = dbm.get_all_events()
                    if event_list:
                        await message.channel.send("Here is a list of events in the database: " + ", ".join(event_list))
                    else:
                        await message.channel.send("There are no events in the database.")
                elif args[1] == '-C':
                    """ Show current event """
                    curr_event = dbm.get_current_event()
                    if curr_event:
                        await message.channel.send("The current event is: " + curr_event)
                    else:
                        await message.channel.send("There is no current event. You can create one with the -n flag, or resume one with -r.")
                elif args[1] == '-N':
                    await message.channel.send("Must include the name of the event to create.")
                elif args[1] == '-R':
                    await message.channel.send("Must include the name of the event to join.")
                elif args[1] == '-J':
                    await message.channel.send("Must include your first name.")
                elif args[1] == '-D':
                    await message.channel.send("Must include the name of the event to delete.")
                else:
                    await message.channel.send("Invalid flag.")
            
            elif len(args) == 3:
                if args[1] == '-N':
                    """ New event """
                    # We have a new event to create
                    # Create database with all the tables
                    if re_validEventName(args[2]):
                        # create category and channels
                        categ = await message.guild.create_category(args[2])
                        await categ.create_text_channel("general")
                        await categ.create_text_channel("info")
                        await categ.create_voice_channel("chat")
                        # create dbs
                        dbm.create_event(args[2], categ.id)
                        await message.channel.send("Created new event: " + args[2] + ". This is now the active event.")
                    else:
                        await message.channel.send("Invalid event name. Use only letters, numbers and dashes.")

                elif args[1] == '-R':
                    """ Resume event """
                    # Check to see if event exists, then make it active
                    if re_validEventName(args[2]):
                        event_list = dbm.get_all_events()
                        if args[2] in event_list:
                            # Set this event as active
                            dbm.activate_event(args[2])
                            await message.channel.send("Successfully activated event: " + args[2])
                        else:
                            await message.channel.send("This event does not exist. Either create it with the -n flag, or check your spelling. Case does not matter.")
                    else:
                        await message.channel.send("The event name was invalid. Event names can only include letters, numbers and hyphens.")
                    
                elif args[1] == '-J':
                    """ Member join current event"""
                    if re_validFirstName(args[2]):
                        # Get the current event
                        curr_event = dbm.get_current_event()
                        if curr_event:
                            # There is an event running, add them
                            dbm.member_join_event(message.author.id, args[2], curr_event)
                            # Add a text channel for this person to event category
                            categID = dbm.get_current_event_categid()
                            await discord.utils.get(message.guild.categories, id=categID).create_text_channel(args[2])
                            await message.channel.send("Successfully joined event: " + curr_event)
                        else:
                            # There is no active event or db error
                            await message.channel.send("There is no active event. Create or resume one first.")
                    else:
                        # The first name was invalid
                        await message.channel.send("Your name was either too long or contained invalid characters. Keep it under 255 characters and only use letters and hyphens.")

                elif args[1] == '-D':
                    """ Delete an event from db and all associated categories/channels """
                    if re_validEventName(args[2]):
                        # Check if this is a valid event
                        event_list = dbm.get_all_events()
                        if args[2] in event_list:
                            # Event name was valid, verify deletion
                            await message.channel.send("Are you sure you want to delete " + args[2] + "? This will delete all text and voice channels. (y/n)")
                            inp = await client.wait_for('message', check=pred)
                            if inp.content.upper() == "Y":
                                # Go for deletion
                                # Get the category
                                categID = dbm.get_event_categid(args[2])
                                categ = discord.utils.get(message.guild.categories, id=categID)
                                # Delete text and voice channels
                                for channel in categ.text_channels:
                                    await channel.delete()
                                for vc in categ.voice_channels:
                                    await vc.delete()
                                # Delete the category
                                await categ.delete()
                                # Deactivate event and clear users from events in db
                                dbm.event_deletion(args[2])
                                await message.channel.send("Done!")
                            else:
                                await message.channel.send("Cancelling...")
                        else:
                            await message.channel.send("This event does not exist.")
                    else:
                        await message.channel.send("The event name was invalid. Event names can only include letters, numbers and hyphens.")

                else:
                    await message.channel.send("Invalid use of command.")

            else:
                await message.channel.send("Invalid number of arguments.")

# Connect to discord and come online
client.run(configs["secret"])