#!/usr/bin/env python3.5
from config import discord_config
import discord, asyncio
from Poorganiser import Poorganiser
import shlex, datetime

client = discord.Client()
porg = Poorganiser()

def idToUsername(members, userID):
    for member in members:
        if int(member.id) == userID:
            return member.name
    return name

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    content = message.content
    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif content.strip() == '!register':
        user_exists = porg.get_user(message.author.id)
        if not user_exists:
            porg.add_user(message.author.id)
            await client.send_message(message.channel, 'Registered user {} with id {}.'.format(message.author.display_name, message.author.id))
        else: # User already exists
            await client.send_message(message.channel, 'You have already registered!')
    elif content.startswith('!help'):
        await client.send_message(message.channel, 'TEMP: HELP: I\'M SO HELPFUL LOL')
    elif content.strip() == "!curr":
        pass
    elif content.strip() == "!past":
        pass
    elif content.strip() == "!survey":
        pass
    elif content.strip() == "!mystatus":
        user = porg.get_user(message.author.id)
        status_message = ""
        if not user:
            status_message += 'Not registered! Use !register'
        else:
            status_message += 'Registered user {} with id {}.\n'.format(message.author.display_name, message.author.id)
            status_message += "Your events:\n"

        await client.send_message(message.channel, status_message)

    else: #multi argument commands
        splits = shlex.split(content)
        admin_commands = ["!create", "!edit", "!delete", "!add", "!remove"]
        cmd = splits[0]
        if cmd == "!poll":
            pass
        elif cmd == "!vote":
            pass
        elif cmd == "!ans":
            pass
        elif cmd == "!event":
            pass
        elif cmd in admin_commands:
            userID = message.author.id
            if True: #TODO IF IS ADMIN
                if cmd == "!create":
                    if len(splits) <= 2 or len(splits) > 7:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !create event <name> OPTIONAL: <location> <year> <month> <day>')
                    elif splits[1] != "event":
                        await client.send_message(message.channel, 'Unknown creation type')
                    else:
                        event_name = splits[2]
                        location = "Undecided"
                        year, month, day = None, None, None
                        try:
                            location = splits[3]
                            year = splits[4]
                            month = splits[5]
                            day = splits[6]
                        except IndexError:
                            year, month, day = None, None, None #if error occured somewhere above, set date back to none
                        new_event = porg.add_event(userID, event_name, location, year, month, day)
                        newID = new_event.get_id()
                        porg.update(new_event)
                        await client.send_message(message.channel, 'New event with ID {} created'.format(newID))
                        members = message.channel.get_all_members()
                        for member in members:
                            eu = porg.add_eventuser(newID, member.id(), "Invited")
                            porg.update(eu)
                        await client.send_message(message.channel, 'All members of channel invited. See !mystatus to check')
                elif cmd == "!edit":
                    if len(splits) < 4:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !edit <eventID> <field> <new_value>')
                    else:
                        eventID = splits[1]
                        edit_event = porg.get_event(eventID)
                        if not edit_event:
                            await client.send_message(message.channel, 'Event not found')
                        elif edit_event.get_ownerid() != int(userID):
                            print("DEBUG: COMPARING DB VALUE |{}| to USERID VALUE |{}|".format(type(edit_event.get_ownerid()), type(userID)))
                            await client.send_message(message.channel, 'You do not have permission to modify this event')
                        else:
                            edit_field = splits[2].lower()
                            if edit_field == "name":
                                edit_event.set_name(splits[3])
                                porg.update(edit_event)
                                await client.send_message(message.channel, 'Event {}\'s name updated to {}'.format(eventID, splits[3]))
                            elif edit_field == "location":
                                edit_event.set_location(splits[3])
                                porg.update(edit_event)
                                await client.send_message(message.channel, 'Event {}\'s location updated to {}'.format(eventID, splits[3]))
                            elif edit_field == "date":
                                if not len(splits) == 6:
                                    await client.send_message(message.channel, 'Invalid date format. Use <year> <month> <day>')
                                else:
                                    date = datetime.date(splits[3], splits[4], splits[5])
                                    edit_event.set_time(date)
                                    porg.update(edit_event)
                                    await client.send_message(message.channel, 'Event {}\'s date updated to {}'.format(eventID, date))
                            else:
                                await client.send_message(message.channel, 'Invalid field type')
                elif cmd == "!delete":
                    #TODO add confirmation for deletion
                    if len(splits) != 2:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !delete <eventID>')
                    else:
                        if porg.remove(splits[1]):
                            await client.send_message(message.channel, 'Event {} was removed'.format(splits[1]))
                        else:
                            await client.send_message(message.channel, 'Remove failed, double check your event ID')
                elif cmd == "!add":
                    pass
                elif cmd == "!remove":
                    pass
            else:
                await client.send_message(message.channel, 'You do not have permission to do that')


client.run(discord_config.token)
