import re
import calendar
import asyncio
import time
import discord

from modules.api import gw2
from modules.tdt import scoreboard
from modules.util import storage
from modules.util import debug
from modules.util import send
from modules.data import private
from modules.data import misc
from datetime import datetime
import threading

_guild = None
_gen_channel = None
_bot_channel = None
update_loop = None


async def pearl_tick(guild, chan):
    debug.debug(debug.D_VERBOSE, 'Running pearl_tick...')
    if _guild is None:
        debug.debug(debug.D_VERBOSE, 'Guild is not set yet... waiting.')
        pass
    else:
        try:
            _now = datetime.now()
            _next = storage.get_server_attribute(guild.id, 'next_pearl_point_reset_datetime')
            debug.debug(debug.D_VERBOSE, 'Current time: {} Next reset: {}'.format(
                _now.strftime('%H:%M:%S'), _next.strftime('%H:%M:%S')))
            if _now > _next:
                await send.message(chan, scoreboard.reset_points_to_give(guild))
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
            storage.set_server_attribute(_guild.id, 'next_pearl_point_reset_datetime', y)
        except AttributeError as e:
            debug.debug(debug.D_ERROR, e)
        debug.debug(debug.D_VERBOSE, 'Time to next reset: {}'.format(
            (storage.get_server_attribute(guild.id, 'next_pearl_point_reset_datetime') - datetime.now())))


async def update():
    global _guild
    global _gen_channel
    debug.debug(debug.D_VOMIT, 'Staring TDT update coroutine...')
    while True:
        debug.debug(debug.D_VOMIT, 'TDT Updating.')
        await pearl_tick(_guild, _gen_channel)

    # if it's past that time, reset.
        await asyncio.sleep(10)

# Update = threading.Thread(target=tick, name='tdtUpdate')


async def on_ready(client, loop):
    """
    Called when we're ready to start tasks from TDT's module.
    :param client: the client from the main module that called this.
    :type client: discord.Client()
    :param loop: The loop we're going to tie TDT's update loop to.
    :type loop: asyncio.AbstractEventLoop()
    :return:
    """

    debug.debug(debug.D_INFO, 'Initializing TDT+ module.')

    global _gen_channel
    global _bot_channel
    global _guild
    global update_loop
    debug.debug(debug.D_VERBOSE, 'Collecting server info...')
    for server in client.guilds:
        debug.debug(debug.D_VOMIT, '{}:{} == {}'.format(
            server.id, private.tdt_server_id, server.id == private.tdt_server_id))
        if server.id == private.tdt_server_id:
            _guild = server
            debug.debug(debug.D_VERBOSE, 'Server locked in...\nFinding channels...')
            for channel in server.channels:
                if channel.name == 'general':
                    _gen_channel = channel
                    debug.debug(debug.D_VERBOSE, 'General channel locked in...')
                elif channel.name == 'bot-test-chat':
                    _bot_channel = channel
                    debug.debug(debug.D_VERBOSE, 'Bot channel locked in...')
    update_loop = asyncio.run_coroutine_threadsafe(update(), loop=loop)
    if _gen_channel is not None and _bot_channel is not None and _guild is not None:
        debug.debug(debug.D_INFO, 'TDT+ initialized')
    else:
        debug.debug(debug.D_ERROR, 'TDT+ did not fully initialize...')
        if _guild is None:
            debug.debug(debug.D_ERROR, 'Couldn\'t lock in the server.')
        if _gen_channel is None:
            debug.debug(debug.D_ERROR, 'Couldn\'t find the general channel.')
        if _bot_channel is None:
            debug.debug(debug.D_ERROR, 'Couldn\'t find the bot channel.')


async def handle_message(client, message, TALKATIVE):
    global update_loop
    debug.debug(debug.D_VERBOSE, 'Entering TDT module.')

    m = message.content.lower()

    # respond to solo fractal emote and give daily fractals
    if '<:fractals:230520375396532224>' in m:
        # await client.send_typing(message.channel)
        response = '```haskell\nDaily Fractals:\n\n'
        t = ''
        r = ''
        fractal_dailies = gw2.get_fractal_dailies()
        ids = []
        for daily in fractal_dailies:
            ids.append(daily['id'])
        names = gw2.get_achievement_names(ids)
        for name in names:
            if ' Tier ' in name and ' 4 ' in name:
                n = re.split(' 4 ', name)[1]
                t = '{}tier 4: {}\n'.format(t, n)
            elif ' Tier ' not in name:
                scale = re.split('Scale ', name)[1]
                n = gw2.get_fractal_name(int(scale))
                r = '{}scale: {} {}\n'.format(r, scale, n)
        await send.message(message.channel, '{}{}\n{}\n```'.format(response, r, t))
        # handled = True

    # end fractals

    # Add reactions to some messages

    if 'treebs' in m or 'omega' in m or 'leftovers' in m and TALKATIVE:
        r = discord.Reaction(message=message, data=None, emoji='treebs:235655554465398784')
        # I don't know what the 'message' and 'data' params are doing here...
        debug.debug(debug.D_INFO, 'Treebs was here...')
        await send.reaction(message, r)

    # End adding reactions

    # direct mention commands

    for mention in message.mentions:  # when someone is mentioned
        debug.debug(debug.D_VERBOSE, '{} was mentioned'.format(mention))
        if mention == client.user:  # if the bot is mentioned
            debug.debug(debug.D_VERBOSE, 'A mention other than the bot was caught.')
            # handled = False
            response = ''

            # -- pearl points --

            if ('give' in m or '+1' in m) and ('pearlpoint' in m or 'pearl point' in m or (
                    'pearl' in m and 'point' in m) or 'point' in m) and '!resetpointstogive' not in m:
                debug.debug(debug.D_VERBOSE, 'Pearl points are being given.')
                response = scoreboard.give_points(client, message)
                # handled = True
            elif ('take' in m or 'remove' in m or '-1' in m) and (
                            'pearlpoint' in m or 'pearl point' in m or ('pearl' in m and 'point' in m) or 'point' in m):
                response = scoreboard.take_points(client, message)
                # handled = True
            elif 'how many points' in m or 'how many pearlpoints' in m or (
                        'how' in m and 'many' in m and 'points' in m):
                if ' i ' in m:
                    debug.debug(debug.D_INFO, 'Fetching remaining points for {}.'.format(message.author))
                    response = scoreboard.read_points_to_give(client, message)
                    # handled = True
                else:
                    response = scoreboard.read_points(client, message)
                    # handled = True
            elif 'who\'s winning' in m or 'leaderboard' in m or 'scoreboard' in m:
                if 'beta' not in m:
                    response = scoreboard.get_top_points()
                elif 'beta' in m:
                    await send.message(message.channel, embed=scoreboard.get_top_points(True))
                # handled = True
            debug.debug(debug.D_VERBOSE, '{}, {}'.format(message.author.id, private.anaeon_id))

            # -- end pearl points --

            # -- dailies --

            if re.search('\\bfractal(\\b|s)|\\bfric frac(\\b|s)', m):
                response = '```haskell\nToday\'s daily fractals:\n\n'
                t = ''
                r = ''
                fractal_dailies = gw2.get_fractal_dailies()
                ids = []
                for daily in fractal_dailies:
                    ids.append(daily['id'])
                names = gw2.get_achievement_names(ids)
                for name in names:
                    if ' Tier ' in name and ' 4 ' in name:
                        t = '{}{}\n'.format(t, name)
                    elif ' Tier ' not in name:
                        scale = re.split('Scale ', name)[1]
                        n = gw2.get_fractal_name(scale)
                        r = '{}Daily {}, Scale {}\n'.format(r, n, scale)
                response = '{}{}\n{}\n```'.format(response, r, t)
                # handled = True

            # -- end dailies --

            # -- general commands --

            # -- end general commands --

            # commands unique to myself
            if str(message.author.id) == private.anaeon_id:
                if '!resetpearlpoints' in m:
                    response = scoreboard.reset_points(client, message)
                    # handled = True
                if '!initpearlpoints' in m:
                    response = scoreboard.init_points_to_give(message)
                    # handled = True
                if '!resetpointstogive' in m:  # forces daily-like reset.
                    response = scoreboard.reset_points_to_give(message.guild)
                    # handled = True
                if '!changeattribute' in m:
                    args = m.split(',')
                    response = scoreboard.force_change_attribute(client, message, args[2].strip(), args[3].strip())
                    # handled = True
                if '!let' in m:
                    await send.message(message.channel, 'This command is broken. Please update.')
                    # await send.message(message.channel, embed = scoreboard.get_top_points(use_embed = True))

            if response != '':
                await send.message(message.channel, response)
                # handled = True
                # end direct mention commands


async def on_exit():
    global update_loop
    update_loop.cancel()
