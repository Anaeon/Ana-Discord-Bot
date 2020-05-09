import discord
import time
import random
import re
import os
import asyncio
import hashlib

from modules.tdt import tdt
from modules.util import debug
from modules.data import strings
from modules.data import private
from modules.data import misc
from modules.api import trump
from modules.util import send

client = discord.Client()

TALKATIVE = False
CAN_DELETE = True


async def send_talk(_svr, _ch, msg):
    """Sends a custom message to a specific server."""

    #  slot in the intended server
    svr = ''
    svr_found = False
    for server in client.guilds:
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
    d = '{}{}{}'.format(misc.CACHE_DIRECTORY, 'images/', animal)
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
            # await client.send_typing(message.channel)
            os.rename('{}/{}'.format(d, filename), '{}/too big/{}'.format(d, filename))
            await send.message(message.channel, 'File moved.')


async def make_md5_hash(_dir, fn):
    dat = open(_dir + '/' + fn, 'r+b')
    ext = fn.split('.')[-1]
    md5hashname = hashlib.md5(dat.read()).hexdigest()
    dat.close()
    debug.debug(debug.D_VERBOSE, 'Checking ' + fn)
    if fn == md5hashname + '.' + ext:
        debug.debug(debug.D_VERBOSE, 'File is already hashed... skipping.')
    elif os.path.exists(_dir + '/' + md5hashname + '.' + ext):
        debug.debug(debug.D_VERBOSE, 'File already exists... deleting duplicate')
        os.remove(_dir + fn)
    elif fn is not md5hashname + '.' + ext:
        debug.debug(debug.D_VERBOSE, 'Hashing file...')
        os.rename(_dir + '/' + fn, _dir + '/' + md5hashname + '.' + ext)


async def hash_images():
    debug.debug(debug.D_INFO, 'Hashing image files.')
    d = '{}{}'.format(misc.CACHE_DIRECTORY, 'images/')
    for _dir in os.listdir(d):
        for fn in os.listdir(d + '/' + _dir):
            if os.path.isfile(d + '/' + _dir + '/' + fn):
                await make_md5_hash(d + _dir, fn)


@client.event
async def on_connect():
    print('Connected')


@client.event
async def on_disconnect():
    print('Disconnected')


@client.event
async def on_ready():
    global client
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # await client.change_presence(activity=discord.Activity(name="with quantum strings."))
    print('------')
    print('Wrapper version: ' + discord.__version__)
    print('------')
    print('debug.DEBUG: {}'.format(debug.DEBUG))

    await hash_images()

    asyncloop = asyncio.get_event_loop()

    await tdt.on_ready(client, asyncloop)
    debug.on_ready()


@client.event
async def on_message_edit(before, after):
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
            debug.debug(debug.D_INFO, 'A unacceptable word was used... attempting to delete it.')
            await send.message(after.channel, 'Noooo... nice try though.')

    # handle edited tdt commands
    if is_tdt:
        await tdt.handle_message(client, after)
    else:
        await on_message(after)

discord.message
@client.event
async def on_message(message):  # when someone sends a message. Read command inputs here.
    global CAN_DELETE
    global TALKATIVE
    m_guild = 'Unknown'
    m_guild_id = 'None'
    m_channel = 'Unknown'
    m_channel_id = 'None'
    if message.guild is not None:
        m_guild = str(message.guild)
        m_guild_id = str(message.guild.id)

    if message.channel is not None:
        m_channel = str(message.channel)
        m_channel_id = str(message.channel.id)

    debug.debug(debug.D_INFO, '[G:{}][C:{}][A:{}]:{}'.format(m_guild, m_channel, message.author, message.content))
    debug.debug(debug.D_VERBOSE, '[G:{}][C:{}][A:{}]'.format(m_guild_id, m_channel_id, message.author.id))

    # go ahead and check which server we're in
    is_tdt = False
    is_neon = False
    is_durg = False
    is_tdt = m_guild_id == private.tdt_server_id

    m = message.content.lower()
    if message.author != client.user:  # don't react to your own messages.

        # Do these things in general...

        if re.search('\\bshut up\\b', m):
            debug.debug(debug.D_INFO, 'Silencing the bot.')
            TALKATIVE = False
            await send.message(message.channel, 'Understood.')
            debug.debug(debug.D_INFO, 'Silencing the bot.')

        if re.search('\\bspeak up\\b', m):
            debug.debug(debug.D_INFO, 'Unsilencing the bot.')
            TALKATIVE = True
            await send.message(message.channel, 'Understood.')

        if re.search('\\bdelete stuff\\b', m):
            # if hasattr(client, discord.Permissions.manage_messages):
            debug.debug(debug.D_INFO, 'Deleting things from this point.')
            CAN_DELETE = True
            await send.message(message.channel, 'Understood.')
            # else:
                # await send.message(message.channel, 'I do not have permission to do that from the server\'s owner.')

        if re.search('\\bdo not delete stuff\\b', m):
            debug.debug(debug.D_INFO, 'Deleting things from this point.')
            CAN_DELETE = False
            await send.message(message.channel, 'Understood.')

        # get a random Trump quote because why the fuck not?

        if re.search('\\btrump\\b|\\bgyna\\b', m):
            await send.typing(message.channel)
            msg = trump.get_quote()
            await send.message(message.channel, '"{}" - Lord Emperor The Donald Trump'.format(msg))

        # end trump

        if re.search('\\broll\\b', m):
            sm = m.replace(' ', '')
            sresult = re.search('(?<=roll)*\d+d\d+', sm)
            if re.search('d\d+', sm):
                if sresult is None:
                    sresult = re.search('(?<=roll)*d\d+', sm)
                if sresult is None:
                    pass
                roll = sresult.group(0)
                # try:
                #    roll = re.search('(?<=roll)*\d+d\d+', sm).group(0)
                # except:
                #    roll = re.search('(?<=roll)*d\d+', sm).group(0)
                #    pass
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

                    elif re.search('\\b3\\b|vomit', m):
                        debug.D_CURRENT_LEVEL = debug.D_VOMIT
                        await send.message(message.channel, 'Now logging EVERYTHING.')

                if '!embedtest' in m:
                    embed = discord.Embed(title='', color=misc.ANA_COLOR)
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
                    await client.change_presence(activity=g_obj)
                    # await client.change_status(game=g_obj) # depricated
                    debug.debug(debug.D_VERBOSE, 'POST-AWAIT THING')

                if '!cleanimagecache' in m:
                    await send.message(message.channel, 'Cleaning up my image cache...')
                    await hash_images()
                    await send.message(message.channel, 'Done.')

        # end basic personal commands

        # end general stuff

        # STUPID STUFF GOES HERE ============================

        if hasattr(message.author, 'nick') and message.author.nick is not None and TALKATIVE:
            if 'duck' in message.author.nick.lower():
                await send.message(message.channel, 'Quack.')
            if 'goose' in message.author.nick.lower():
                await send.message(message.channel, 'Honk.')
            if 'fox' in message.author.nick.lower():
                await send.message(message.channel, 'Yiff.')

        for regex in strings.no_words_regex:
            debug.debug(debug.D_VOMIT, 'Checking for {} in "{}".'.format(regex, m))
            if re.search(regex, m):
                debug.debug(debug.D_INFO, 'A unacceptable word was used... attempting to delete it.')
                if CAN_DELETE:
                    try:
                        await message.delete()
                    except PermissionError as e:
                        debug.debug(debug.D_ERROR, e)
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
            await send_animal(message, 'fox')  # No, because an elif would mean it can't catch multiple in the same msg.
        # HONK
        if re.search('\\bhonk\\b', m):
            await send_animal(message, 'goose')

        for mention in message.mentions:

            if mention == client.user and TALKATIVE:
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
            await tdt.handle_message(client, message, TALKATIVE)

        # @client.event
        # async def on_reaction_add(reaction, user): # when someone adds a reaction?
        # do nothing


@client.event
async def on_exit():
    await tdt.on_exit()
    debug.on_exit()


client.run(private.token)
