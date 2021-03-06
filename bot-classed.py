import discord
import time
import random
import re
import os

from modules.tdt import tdt
from modules.util import debug
from modules.data import strings
from modules.data import private
from modules.api import trump
from modules.util import send

client = discord.Client()

ANA_COLOR = int('4408a3', 16)


async def send_talk(_svr, _ch, msg):
    """Sends a custom message to a specific server."""

    #  slot in the intended server
    svr = ''
    svr_found = False
    for server in client.servers:
        if server.name == _svr:
            svr = server
            svr_found = True

    if not svr_found:  # if the bot is not part of the server or the server can't be found, say so
        await send.message(client.get_channel(private.anaeon_dm_id),
                           'No server found with name {}.'.format(_svr))
    elif svr_found:  # else, try to slot in the channel
        ch = ''
        ch_found = False
        for channel in svr.channels:
            if channel.name == _ch:
                ch = channel
                ch_found = True

        if not ch_found:  # if the bot can't find the channel in the server, say so
            await send.message(client.get_channel(private.anaeon_dm_id),
                               'No channel found with name {}.'.format(_ch))
        elif ch_found:  # else, go ahead and format the message and send it to the channel.
            if msg == '':
                await send.message(client.get_channel(private.anaeon_dm_id), 'I can\'t send a blank message.')
            else:
                await send.message(ch, msg)


async def send_animal(message, animal):
    """
    Sends a random image of the given animal to the channel.
    :param message: The message that caused this to run.
    :type message: discord.Message
    :param animal: A string representing the name of the animal to send.
    :type animal: str
    """
    d = 'D:/Users/Anaeon/Dropbox/Ana Cache/{}'.format(animal)
    filename = random.choice([x for x in os.listdir(d) if os.path.isfile(d + "/" + x)])
    path = os.path.join(d, filename)
    with open(path, 'rb') as file:
        try:
            await send.file(message.channel, discord.File(file))
        except discord.HTTPException as e:
            # Check for what kind of exception it is before trying to move a file that doesn't exist
            # thereby raising another exception
            await send.message(message.channel, e)
            time.sleep(2)
            await send.message(message.channel, 'Error encountered on file "{}/{}"'.format(d, filename))
            # I want to have Ana move any files that are too large into the appropriate folder.
            await send.message(message.channel, 'Moving file to another folder to avoid the error.')
            await client.send_typing(message.channel)
            os.rename('{}/{}'.format(d, filename), '{}/too big/{}'.format(d, filename))
            await send.message(message.channel, 'File moved.')


class Client(discord.Client):

    async def on_connect(self):
        print('Connected')

    async def on_disconnect(self):
        if tdt.Update.is_alive():
            tdt.Update.stop()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(client.user.id)
        await client.change_presence(activity=discord.Activity(name="with quantum strings."))
        print('------')
        print(discord.__version__)
        print('------')
        print('debug.DEBUG: {}'.format(debug.DEBUG))
        if tdt.Update.isAlive():
            pass
        else:
            tdt.Update.start()
        await tdt.on_ready(self)

    async def on_message_edit(self, before, after):
        #  b_m = before.content.lower()
        a_m = after.content.lower()

        # go ahead and check which server we're in
        is_tdt = False
        #  is_neon = False
        #  is_durg = False
        try:
            is_tdt = str(after.guild.id) == private.tdt_server_id
        except AttributeError as e:
            debug.debug(debug.D_ERROR,
                        'Caught AttributeError while trying to determine what server a message came from. {}'.format(e))

        # handle sneaky no_words
        for regex in strings.no_words_regex:
            if re.search(regex, a_m):
                debug.debug(debug.D_INFO, 'A unacceptable word was used... attemting to delete it.')
                await send.message(after.channel, 'Noooo... nice try though.')

        # handle edited tdt commands
        if is_tdt:
            await tdt.handle_message(client, after)

    async def on_message(self, message):  # when someone sends a message. Read command inputs here.
        m_guild = 'Unknown'
        m_channel = 'Unknown'
        if message.guild is not None:
            m_guild = str(message.guild)

        if message.channel is not None:
            m_channel = str(message.channel)

        debug.debug(debug.D_INFO, '[{}][{}][{}]:{}'.format(m_guild, m_channel, message.author, message.content))

        # go ahead and check which server we're in
        is_tdt = False
        is_neon = False
        is_durg = False
        try:
            is_tdt = str(message.guild.id) == private.tdt_server_id
        except AttributeError as e:
            debug.debug(debug.D_ERROR,
                        'AttributeError caught: {}'.format(e))

        m = message.content.lower()
        if message.author != client.user:  # don't react to your own messages.

            # Do these things in general...

            # get a random Trump quote because why the fuck not?

            if re.search('\\btrump\\b|\\bgyna\\b', m):
                await send.typing(message.channel)
                msg = trump.get_quote()
                await send.message(message.channel, '"{}" - Lord Emperor The Donald Trump'.format(msg))

            # end trump

            if re.search('\\broll\\b', m):
                sm = m.replace(' ', '')
                if re.search('d\d+', sm):
                    try:
                        roll = re.search('(?<=roll)*\d+d\d+', sm).group(0)
                    except:
                        roll = re.search('(?<=roll)*d\d+', sm).group(0)
                        pass
                    debug.debug(debug.D_INFO, 'roll == {}'.format(roll))
                    request = roll.split('d', 1)
                    rolls = 1
                    if request[0] != '':
                        rolls = int(request[0])
                    debug.debug(debug.D_INFO, 'rolls == {}'.format(rolls))
                    die = int(request[1])
                    debug.debug(debug.D_INFO, 'die == {}'.format(die))

                    max_rolls = 10

                    if rolls > max_rolls:
                        await send.message(message.channel, 'Yeah... I\'m only rolling {} times.'.format(max_rolls))
                        time.sleep(2)
                        if rolls > max_rolls + 10:
                            await send.message(message.channel, 'Fuck you.')
                        time.sleep(3)
                        rolls = max_rolls
                    if die == 0:
                        await send.message(message.channel, strings.roll_zero(message))
                    else:
                        if rolls == 0:
                            await send.message(message.channel, 'You want me to roll zero d{}\'s?'.format(die))
                            time.sleep(3)
                            await send.message(message.channel, '... well, I guess I\'m done then.')
                        elif rolls < 2:
                            await send.message(message.channel, 'Rolling a d{}.'.format(die))
                        else:
                            await send.message(message.channel, 'Rolling {} d{}\'s.'.format(rolls, die))
                        time.sleep(2)
                        for i in range(rolls):
                            n = random.randint(1, die)
                            await send.message(message.channel, '*Roll {}*: {}.'.format(i + 1, n))
                            time.sleep(2)

            # basic personal commands

            #  private message commands
            if str(message.channel.id) == private.anaeon_dm_id:

                if m.startswith('!talk'):
                    args = message.content.split(',')
                    msg = ''
                    for i in range(len(args)):
                        if i == 3:
                            #  add in the first chunk of message
                            msg = '{}{}'.format(msg, args[i])
                        elif i > 3:
                            #  add in the rest of the chunks including commas to replace those lost by re.split()
                            msg = '{},{}'.format(msg, args[i])
                    await send_talk(args[1].strip(), args[2].strip(), msg.strip())

            for mention in message.mentions:
                if mention == client.user and str(message.author.id) == private.anaeon_id:
                    if '!debugon' in m:
                        if debug.DEBUG:
                            await send.message(message.channel, 'Debug was already active.')

                        elif not debug.DEBUG:
                            debug.DEBUG = True
                            await send.message(message.channel, 'Debug is now active at {} level.'.format(
                                debug.D_HEADER[debug.D_CURRENT_LEVEL]))

                    if '!debugoff' in m:
                        if debug.DEBUG:
                            debug.DEBUG = False
                            await send.message(message.channel, 'Debug is now off.')

                        elif not debug.DEBUG:
                            await send.message(message.channel, 'Debug was already off.')

                    if '!debuglevel' in m:
                        if re.search('\\b0\\b|error', m):
                            debug.D_CURRENT_LEVEL = debug.D_ERROR
                            await send.message(message.channel, 'Now logging debug at ERROR level.')

                        elif re.search('\\b1\\b|info', m):
                            debug.D_CURRENT_LEVEL = debug.D_INFO
                            await send.message(message.channel, 'Now logging debug at INFO level and below.')

                        elif re.search('\\b2\\b|verbose', m):
                            debug.D_CURRENT_LEVEL = debug.D_VERBOSE
                            await send.message(message.channel, 'Now logging debug at VERBOSE level and below.')

                    if '!embedtest' in m:
                        embed = discord.Embed(title='', color=ANA_COLOR)
                        embed.set_author(name='Test Author Name')
                        embed.add_field(name='Test Field 1', value='Test Value')
                        embed.add_field(name='Test Field 2', value='s;laksdfj')
                        embed.add_field(name='Multi-line', value='other\nstuff', inline=True)
                        embed.set_footer(text='Test Footer Text')
                        await send.message(message.channel, embed=embed)

                    if '!status' in m:
                        g = re.search('(?<=game=).+', m).group(0)
                        g_obj = discord.Game(name=g)
                        debug.debug(debug.D_VERBOSE, 'game object = {}'.format(g_obj))
                        debug.debug(debug.D_VERBOSE, 'Setting status to \"Playing {}\".'.format(g))
                        await client.change_presence(game=g_obj)
                        # await client.change_status(game=g_obj) # depricated
                        debug.debug(debug.D_VERBOSE, 'POST-AWAIT THING')

            # end basic personal commands

            # end general stuff

            # STUPID STUFF GOES HERE ============================

            if message.author.nick is not None:
                if 'duck' in message.author.nick.lower():
                    await send.message(message.channel, 'Quack.')
                if 'goose' in message.author.nick.lower():
                    await send.message(message.channel, 'Honk.')

            for regex in strings.no_words_regex:
                debug.debug(debug.D_VERBOSE, 'Checking for {} in "{}".'.format(regex, m))
                if re.search(regex, m):
                    debug.debug(debug.D_INFO, 'A unacceptable word was used... attempting to delete it.')
                    # await client.delete_message(message)
                    r = strings.no_words_response
                    response = (r[random.randint(1, len(r)) - 1])
                    await send.message(message.channel, response)

                    time.sleep(2)

            if re.search('\\bfag(\\b|s)|\\bfaggot(\\b|s)|\\bfaggotry\\b|\\bgay(\\b|s)|\\bga{2,99}y(\\b|s)|\\blgbt\\b', m):
                debug.debug(debug.D_INFO, 'Reacting to some faggotry.')
                try:
                    await send.reaction(message, '🏳️‍🌈')
                except discord.errors.HTTPException as e:
                    debug.debug(debug.D_ERROR, e)

            # GIV DEM BITCHES SOME LIZARDS
            if re.search('\\blizard(\\b|s)', m):
                await send_animal(message, 'lizard')

            # GIV DEM BITCHES SOME FOXES
            if re.search('\\bfox(\\b|s)', m):  # Fold all of these into a big elif somehow.
                await send_animal(message, 'fox')

            for mention in message.mentions:

                if mention == client.user:
                    if 'anal' in m:
                        r = [
                            'I guess... if I open up the right ports.',
                            'That\'s not supposed to go there!',
                            '```Throughput error:\n\nIncorrect dataflow direction.```'
                        ]
                        response = (r[random.randint(1, len(r)) - 1])
                        await send.message(message.channel, response)

                    if 'suck' in m:
                        r = [
                            'Sorry, {}, I\'m not scripted for that kind of thing...'.format(message.author.mention),
                            'I can get you a vacuum, if you\'d like.',
                            '```Packet error:\n\nSize smaller than expected.```'
                        ]
                        response = (r[random.randint(1, len(r)) - 1])
                        await send.message(message.channel, response)

                    if 'lick' in m:
                        r = [
                            'I don\'t exactly have a tongue, {}...'.format(message.author.mention),
                            'People don\'t usually ask for stuff like that from anything python-related,'
                            'but everyone has their kinks, I guess.',
                            '```Error:\n\nPeripheral device driver not found.```'
                        ]
                        response = (r[random.randint(1, len(r)) - 1])
                        await send.message(message.channel, response)

                    if 'smash or pass' in m:
                        await send.message(message.channel, random.choice(['smash', 'pass']))

                    # END STUPID STUFF =================================

                    # SIMPLE RESPONSES =================================

                    if re.search('\\bthank(\\b|s)', m):
                        await send.message(message.channel, strings.youre_welcome(message))

                    if re.search('\\bhi\\b|\\bhey\\b|\\bhello\\b|\\bwhat\'s up\\b', m):
                        await send.message(message.channel, strings.hi(message))

            # END SIMPLE RESPONSES =================================

            # Begin per-server message handling.

            # Only do these things in Digital Table server.

            if is_tdt:
                await tdt.handle_message(client, message)

            # @client.event
            # async def on_reaction_add(reaction, user): # when someone adds a reaction?
            # do nothing

    async def on_exit(self):
        pass


Client.run(private.token)
