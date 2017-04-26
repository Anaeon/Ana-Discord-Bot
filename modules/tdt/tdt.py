import re

from modules.api import gw2
from modules.tdt import scoreboard
from modules.util import storage
from modules.util import debug
from modules.data import private
from datetime import datetime


async def handle_message(client, message):
    # check if alloted points for the day should be reset yet.
    m = message.content.lower()
    try:
        if datetime.now() > storage.get_server_attribute(message.server.id, 'next_pearl_point_reset_datetime'):
            await client.send_message(message.channel, scoreboard.reset_points_to_give(message.server))
    except KeyError as e:
        debug.debug(debug.D_ERROR, e)
        x = datetime.today()  # today
        if datetime.now().hour < 17:
            y = x.replace(hour = 17, minute = 0, second = 0, microsecond = 0)  # today at 5
        else:
            y = x.replace(day = x.day + 1, hour = 17, minute = 0, second = 0, microsecond = 0)  # tomorrow at 5
        storage.set_server_attribute(message.server.id, 'next_pearl_point_reset_datetime', y)
    debug.debug(debug.D_INFO, 'Time to next reset: {}'.format(
        (storage.get_server_attribute(message.server.id, 'next_pearl_point_reset_datetime') - datetime.now())))
    # if it's past that time, reset.

    # respond to solo fractal emote and give daily fractals

    if '<:fractals:230520375396532224>' in m:
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
                n = gw2.get_fractal_name(scale)
                r = '{}scale: {} {}\n'.format(r, scale, n)
        await client.send_message(message.channel, '{}{}\n{}\n```'.format(response, r, t))

    # end fractals

    # Add reactions to some messages

    if 'treebs' in m or 'omega' in m:
        debug.debug(debug.D_INFO, 'Treebs was here...')
        await client.add_reaction(message, 'treebs:235655554465398784')

    # End adding reactions



    # direct mention commands

    for mention in message.mentions:  # when someone is mentioned
        debug.debug(debug.D_INFO, '{} was mentioned'.format(mention))
        if mention == client.user:  # if the bot is mentioned
            response = ''

            # -- pearl points --

            if ('give' in m or '+1' in m) and ('pearlpoint' in m or 'pearl point' in m or (
                    'pearl' in m and 'point' in m) or 'point' in m) and '!resetpointstogive' not in m:
                response = scoreboard.give_points(client, message)
            elif ('take' in m or 'remove' in m or '-1' in m) and (
                            'pearlpoint' in m or 'pearl point' in m or ('pearl' in m and 'point' in m) or 'point' in m):
                response = scoreboard.take_points(client, message)
            elif 'how many points' in m or 'how many pearlpoints' in m or (
                        'how' in m and 'many' in m and 'points' in m):
                if ' i ' in m:
                    debug.debug(debug.D_INFO, 'Fetching remaining points for {}.'.format(message.author))
                    response = scoreboard.read_points_to_give(client, message)
                else:
                    response = scoreboard.read_points(client, message)
            elif 'who\'s winning' in m or 'leaderboard' in m:
                response = scoreboard.get_top_points()
            print('{}, {}'.format(message.author.id, private.anaeon_id))

            # -- end pearl points --

            # -- dailies --

            if re.search('\\bfractal(\\b|s)|\\bfric frac(\\b|s)', m):
                response = '```\nToday\'s daily fractals:\n\n'
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

            # -- end dailies --

            # commands unique to myself
            if message.author.id == private.anaeon_id:
                if '!resetpearlpoints' in m:
                    response = scoreboard.reset_points(client, message)
                if '!initpearlpoints' in m:
                    response = scoreboard.init_points_to_give(message)
                if '!resetpointstogive' in m:
                    response = scoreboard.reset_points_to_give(message.server)
                if '!changeattribute' in m:
                    args = m.split(',')
                    response = scoreboard.force_change_attribute(client, message, args[2].strip(), args[3].strip())

            if response != '':
                await client.send_message(message.channel, response)

                # end direct mention commands
