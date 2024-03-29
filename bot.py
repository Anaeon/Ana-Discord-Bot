import discord
import time
import random
import re
import os
import asyncio
import hashlib
import logging
#import GUI
import calendar

from datetime import datetime
from dateutil import parser

from modules.tdt import tdt
from modules.util import debug
from modules.data import strings
from modules.data import private
from modules.data import misc
from modules.api import trump
from modules.api import wordnik
from modules.util import send
from modules.util import storage

intents = discord.Intents(messages=True, members=True, guilds=True)
client = discord.Client(intents=intents)
gui = None

frmt = logging.Formatter(misc.LOGGER_FORMATTING)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

wslog = logging.getLogger('websocket')
wslog.setLevel(logging.DEBUG)

dislog = logging.getLogger('discord.gateway')
dislog.setLevel(logging.DEBUG)

c_out = logging.StreamHandler()
c_out.setFormatter(frmt)

main_update_loop = None

log.addHandler(c_out)
# wslog.addHandler(c_out)
# dislog.addHandler(c_out)

TALKATIVE = False
CAN_DELETE = False
LAST_MESSAGE = None


async def send_talk(_svr, _ch, msg):
    """
    Sends a custom message to a specific server.
    Command Format:
    !talk, server, channel, message_text
    """

    #  slot in the intended server
    svr = ''
    svr_found = False
    for server in client.guilds:
        if server.name == _svr:
            svr = server
            svr_found = True

    if not svr_found:  # if the bot is not part of the server or the server can't be found, say so
        await send.message(client.get_channel(int(private.anaeon_dm_id)),
                           'No server found with name {}.'.format(_svr))
    elif svr_found:  # else, try to slot in the channel
        ch = ''
        ch_found = False
        for channel in svr.channels:
            if channel.name == _ch:
                ch = channel
                ch_found = True

        if not ch_found:  # if the bot can't find the channel in the server, say so
            await send.message(client.get_channel(int(private.anaeon_dm_id)),
                               'No channel found with name {}.'.format(_ch))
        elif ch_found:  # else, go ahead and format the message and send it to the channel.
            if msg == '':
                await send.message(client.get_channel(int(private.anaeon_dm_id)), 'I can\'t send a blank message.')
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
            log.exception(e)
            await send.message(message.channel, e)
            await send.message(message.channel, 'Looks like that file was too large.')
            # I want to have Ana move any files that are too large into the appropriate folder.
            await send.message(message.channel, 'Moving the file to another folder to avoid the error.')
            # await client.send_typing(message.channel)
            os.rename('{}/{}'.format(d, filename), '{}/too big/{}'.format(d, filename))
            await send.message(message.channel, 'File moved.')


async def make_md5_hash(_dir, fn):
    dat = open(_dir + '/' + fn, 'r+b')
    ext = fn.split('.')[-1]
    md5hashname = hashlib.md5(dat.read()).hexdigest()
    dat.close()
    # debug.debug(debug.D_VERBOSE, 'Checking ' + fn)
    log.debug('Checking ' + fn)
    if fn == md5hashname + '.' + ext:
        # debug.debug(debug.D_VERBOSE, 'File is already hashed... skipping.')
        log.debug('File is already hashed... skipping)')
    elif os.path.exists(_dir + '/' + md5hashname + '.' + ext):
        # debug.debug(debug.D_VERBOSE, 'File already exists... deleting duplicate')
        log.debug('File already exists... deleting duplicate.')
        os.remove(_dir + '/' + fn)
    elif fn is not md5hashname + '.' + ext:
        # debug.debug(debug.D_VERBOSE, 'Hashing file...')
        log.debug('Hashing file...')
        os.rename(_dir + '/' + fn, _dir + '/' + md5hashname + '.' + ext)


async def hash_images():
    # debug.debug(debug.D_INFO, 'Hashing image files.')
    log.info('Hashing image files')
    d = '{}{}'.format(misc.CACHE_DIRECTORY, 'images/')
    for _dir in os.listdir(d):
        if _dir != 'desktop.ini':
            for fn in os.listdir(d + '/' + _dir):
                if os.path.isfile(d + '/' + _dir + '/' + fn) and fn != 'desktop.ini':
                    await make_md5_hash(d + _dir, fn)


async def daily():
    #ensure that the timer is reset
    x = datetime.today()  # today
    if datetime.now().hour < 17:
        y = x.replace(hour=17, minute=0, second=0, microsecond=0)  # today at 5pm
    else:
        if x.day + 1 <= calendar.monthrange(x.year, x.month)[1]:
            y = x.replace(day=x.day + 1, hour=17, minute=0, second=0, microsecond=0)  # tomorrow at 5pm
        else:
            if x.month + 1 <= 12:
                #  first day of next month at 5pm
                y = x.replace(month=x.month + 1, day=1, hour=17, minute=0, second=0, microsecond=0)
            else:
                y = x.replace(year=x.year + 1, month=1, day=1, hour=17, minute=0, second=0, microsecond=0)

    delta_t = y - x  # time between now and next reset
    secs = delta_t.seconds + 1

    # t = Timer(secs, resetPointsToGive(server))

    # Fetch the current info before it's actually changed. This is important.
    _now = datetime.now()
    try:
        _next = parser.parse(storage.load_bot_setting('next_daily_datetime'))
    except storage.NoSuchSettingException:
        log.info('No daily reset time has been saved, yet.')
    # Now set the next reset to avoid this line running again.
    storage.save_bot_setting('next_daily_datetime', y)

    debug.debug(debug.D_VOMIT, 'Current time: {} Next reset: {}'.format(
        _now.strftime('%H:%M:%S'), _next.strftime('%H:%M:%S')))
    # Now do the stuff.
    if _now > _next:
        # DO DAILY STUFF HERE
        # TODO: Maybe put a method here and close this block as a helper to simplify readability.
        await tdt.daily()

        # NO DAILY STUFF PAST THIS LINE

# TODO: Delete this method. I don't think I'm using it.
async def daily_old():
    try:
        _now = datetime.now()
        _next = storage.load_bot_setting('next_wotd_datetime')
        debug.debug(debug.D_VOMIT, 'Current time: {} Next reset: {}'.format(
            _now.strftime('%H:%M:%S'), _next.strftime('%H:%M:%S')))
        if _now > _next:
            # DO DAILY STUFF HERE

            await tdt.daily()

            # NO DAILY STUFF PAST THIS LINE
    except KeyError as e:
        debug.debug(debug.D_ERROR, e)
        x = datetime.today()  # today
        if datetime.now().hour < 17:
            y = x.replace(hour=17, minute=0, second=0, microsecond=0)  # today at 5pm
        else:
            if x.day + 1 <= calendar.monthrange(x.year, x.month)[1]:
                y = x.replace(day=x.day + 1, hour=17, minute=0, second=5, microsecond=0)  # tomorrow at 5pm
            else:
                if x.month + 1 <= 12:
                    #  first day of next month at 5pm
                    y = x.replace(month=x.month + 1, day=1, hour=17, minute=0, second=5, microsecond=0)
                else:
                    y = x.replace(year=x.year + 1, month=1, day=1, hour=17, minute=0, second=5,
                                  microsecond=0)
        storage.save_bot_setting('next_wotd_datetime', y)
    except AttributeError as e:
        debug.debug(debug.D_ERROR, e)
    debug.debug(debug.D_VOMIT, 'Time to next wotd: {}'.format(
        (storage.load_bot_setting('next_wotd_datetime') - datetime.now())))

    # ensure that the timer is reset
    x = datetime.today()  # today
    if datetime.now().hour < 17:
        y = x.replace(hour=17, minute=0, second=0, microsecond=0)  # today at 5pm
    else:
        if x.day + 1 <= calendar.monthrange(x.year, x.month)[1]:
            y = x.replace(day=x.day + 1, hour=17, minute=0, second=0, microsecond=0)  # tomorrow at 5pm
        else:
            if x.month + 1 <= 12:
                #  first day of next month at 5pm
                y = x.replace(month=x.month + 1, day=1, hour=17, minute=0, second=0, microsecond=0)
            else:
                y = x.replace(year=x.year + 1, month=1, day=1, hour=17, minute=0, second=0, microsecond=0)

    delta_t = y - x  # time between now and next reset
    secs = delta_t.seconds + 1

    # t = Timer(secs, resetPointsToGive(server))

    storage.save_bot_setting('next_wotd_datetime', y)


async def update():
    while True:
        # debug.debug(debug.D_VOMIT, 'Running main update loop...')
        log.info('Running main update loop...')
        await daily()
        await asyncio.sleep(30)


@client.event
async def on_connect():
    log.info('Connected')


@client.event
async def on_disconnect():
    log.info('Disconnected.')


@client.event
async def on_ready():
    global client
    global gui
    global main_update_loop
    global LAST_MESSAGE
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(activity=discord.Game(name='with quantum strings.'))
    print('------')
    print('Wrapper version: ' + discord.__version__)
    print('------')
    print('debug.DEBUG: {}'.format(debug.DEBUG))

    await hash_images()

    asyncloop = asyncio.get_event_loop()

    # if gui is None:
        # gui = GUI.on_ready(asyncloop, client)
    storage.on_ready(client)
    debug.on_ready()
    await tdt.on_ready(client, asyncloop)
    main_update_loop = asyncio.run_coroutine_threadsafe(update(), loop=asyncloop)


@client.event
async def on_message_edit(before, after):
    #  b_m = before.content.lower()
    a_m = after.content.lower()

    # go ahead and check which server we're in
    is_tdt = False
    #  is_neon = False
    #  is_durg = False
    try:
        is_tdt = after.guild.id == private.tdt_server_id
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
        await tdt.handle_message(client, after, TALKATIVE)
    else:
        await on_message(after)


@client.event
async def on_message(message):  # when someone sends a message. Read command inputs here.
    global CAN_DELETE
    global TALKATIVE
    global gui

    # gui.add_chat_message(message)

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
    is_neon = False
    is_durg = False
    is_tdt = m_guild_id == str(private.tdt_server_id)
    debug.debug(debug.D_VERBOSE, 'TDT == ' + str(is_tdt))

    m = message.content.lower()
    if message.author != client.user:  # don't react to your own messages.

        # Do these things in general...

        # Only if mentioned
        for mention in message.mentions:
            if mention == client.user:
                if re.search('\\bshut up\\b', m):
                    debug.debug(debug.D_INFO, 'Silencing the bot.')
                    TALKATIVE = False
                    await send.message(message.channel, 'Understood.')

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
                    debug.debug(debug.D_INFO, 'No longer deleting things.')
                    CAN_DELETE = False
                    await send.message(message.channel, 'Understood.')

        if re.search('\\broll\\b', m):
            sm = m.replace(' ', '')
            sresult = re.search('(?<=roll)*\d+d\d+', sm)
            if re.search('d\d+', sm):
                if sresult is None:
                    sresult = re.search('(?<=roll)*d\d+', sm)
                if sresult is None:
                    pass
                roll = sresult.group(0)
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
        if message.channel.id == private.anaeon_dm_id:

            # !talk
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
            if message.author.id != private.anaeon_id:
                pass
            elif mention == client.user and message.author.id == private.anaeon_id:
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
                    # g_obj = discord.Activity(name=g)
                    # debug.debug(debug.D_VERBOSE, 'game object = {}'.format(g_obj))
                    debug.debug(debug.D_VERBOSE, 'Setting status to \"Playing {}\".'.format(g))
                    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=g))
                    # await client.change_status(game=g_obj) # depricated
                    debug.debug(debug.D_VERBOSE, 'POST-AWAIT THING')

                if '!cleanimagecache' in m:
                    await send.message(message.channel, 'Cleaning up my image cache...')
                    await hash_images()
                    await send.message(message.channel, 'Done.')

                if '!reboot' in m or '!restart' in m:
                    await client.get_user(108467075613216768).send('Shutting down.')
                    await client.close()

                if '!exe' in message.content:
                    log.info('Running custom code.')
                    code = message.content.replace('<@!297237845591195651> !exe ', '')
                    locs=locals()
                    new_code = f'async def _ex(locs): '
                    log.debug(code)
                    if 'await' in code or 'async' in code:
                        try:
                            log.info('Running code as async.')
                            for line in code.split('\n'):
                                new_code = new_code + f'\n    ' + line
                            exec(new_code)
                            await locals()['_ex'](locs)
                            # THIS SHIT BE DANGEROUS AS FUCK, YO. PROTECT THAT SHIT.
                            log.debug('Code ran successfully.')
                        except BaseException as e:
                            log.exception('Code failed.')
                            await send.message(message.channel, str(e))
                            await send.message(message.channel, '```python\n' + new_code + '```')
                    else:
                        try:
                            exec(code, globals(), locals())
                            # THIS SHIT BE DANGEROUS AS FUCK, YO. PROTECT THAT SHIT.
                            log.debug('Code ran successfully.')
                        except BaseException as e:
                            log.exception('Code failed.')
                            await send.message(message.channel, str(e))
                            await send.message(message.channel, '```python\n' + code + '```')

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
                    except discord.errors.Forbidden as e:
                        debug.debug(debug.D_ERROR, e)
                    except discord.errors.NotFound as e:
                        debug.debug(debug.D_ERROR, e)
                await send.message(message.channel, strings.no_words_response(message))

                time.sleep(2)

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
    await client.close()  # is this redundant?


client.run(private.token)
