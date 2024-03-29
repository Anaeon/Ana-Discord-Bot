from operator import itemgetter
from datetime import datetime
import calendar

import discord

from modules.data import strings, misc, private
from modules.util import storage
from modules.util import debug

dailyPoints = 1
pointToGiveCap = 3

# TODO: Update this module to use proper logging!!!

def init_points_to_give(message):
    users = message.guild.members
    response = 'The following users have been initialized, and have one point to give:\n\n'
    for user in users:
        try:
            storage.get_user_attribute(message.guild.id, user.id, 'available_pearl_points')
        except KeyError as e:
            storage.set_user_attribute(message.guild.id, user.id, 'available_pearl_points', dailyPoints)
            response = '{}||{}'.format(response, user.mention)

    # also init the server attribute for the datetime of the next reset
    x = datetime.today()  # today
    y = x.replace(day = x.day + 1, hour = 17, minute = 0, second = 0, microsecond = 0)  # tomorrow at 5

    delta_t = y - x  # time between now and next reset
    secs = delta_t.seconds + 1

    storage.set_server_attribute(message.guild.id, 'next_pearl_point_reset_datetime', y)
    return response


def reset_points_to_give(server):

    # This chunk gives the users
    users = server.members
    response = 'The following users have been given new points to use:'
    new_points_given = False

    for user in users:
        user_points_left = 0
        debug.debug(debug.D_INFO, 'Checking ' + str(user.name) +'...')
        try:
            user_points_left = storage.get_user_attribute(server.id, user.id, 'available_pearl_points')
            debug.debug(debug.D_INFO, str(user_points_left) + ' points left.')
            if user_points_left < pointToGiveCap:
                give = user_points_left + dailyPoints
                debug.debug(debug.D_INFO, 'Giving ' + str(dailyPoints) + ' point(s).')
                storage.set_user_attribute(server.id, user.id, 'available_pearl_points', give)
                response = '{}||{}'.format(response, user.mention)
                new_points_given = True
        except KeyError as e:
            debug.debug(debug.D_INFO, 'Skipping Ana...')

    # This chunk sets the reset timer to a specific time tomorrow (or to the proper time today, if it should happen).
    # await client.send_message(server, response)
    debug.debug(debug.D_INFO, 'Points to spend have been reset')
    x = datetime.today()  # today

    if datetime.now().hour < 17:
        y = x.replace(hour = 17, minute = 0, second = 0, microsecond = 0)  # today at 5pm
    else:
        if x.day + 1 <= calendar.monthrange(x.year, x.month)[1]:
            y = x.replace(day = x.day + 1, hour = 17, minute = 0, second = 0, microsecond = 0)  # tomorrow at 5pm
        else:
            if x.month + 1 <= 12:
                #  first day of next month at 5pm
                y = x.replace(month = x.month + 1, day = 1, hour = 17, minute = 0, second = 0, microsecond = 0)
            else:
                y = x.replace(year = x.year + 1, month = 1, day = 1, hour = 17, minute = 0, second = 0, microsecond = 0)

    delta_t = y - x  # time between now and next reset
    secs = delta_t.seconds + 1

    # t = Timer(secs, resetPointsToGive(server))

    storage.set_server_attribute(server.id, 'next_pearl_point_reset_datetime', y)
    if not new_points_given:
        response = strings.no_players()
    return response


def read_points_to_give(client, message):
    id = 'null'
    pearlpointstogive = 0
    response = '... nothing happened ...'
    for mention in message.mentions:
        id = message.author.id

        try:
            pearlpointstogive = int(storage.get_user_attribute(message.guild.id, id, 'available_pearl_points'))
        except KeyError as e:
            debug.debug(debug.D_ERROR, e)
        if pearlpointstogive == 1:
            response = "You have {} pearl point to give.".format(pearlpointstogive)
        else:
            response = "You have {} pearl points to give.".format(pearlpointstogive)
    return response


def give_points(client, message):
    id = 'null'
    pearlpoints = 0
    response = '... nothing happened ...'
    if len(message.mentions) >= 3:
        return 'You can\'t send points to more than one person at a time.'
    for mention in message.mentions:
        debug.debug(debug.D_VERBOSE, 'Checking mention: ' + mention.name)
        debug.debug(debug.D_VERBOSE, 'mention != client.user : ' + str(mention != client.user))
        debug.debug(debug.D_VERBOSE, 'mention != message.author : ' + str(mention != message.author))
        debug.debug(debug.D_VERBOSE, 'mention.bot : ' + str(mention.bot))
        if mention != client.user and mention != message.author and not mention.bot:
            ptg = 0
            try:
                ptg = storage.get_user_attribute(message.guild.id, message.author.id, 'available_pearl_points')
            except KeyError as e:
                debug.debug(debug.D_ERROR, e)
            if ptg > 0:
                id = mention.id
                try:
                    pearlpoints = int(storage.get_user_attribute(message.guild.id, id, "pearl_points"))
                except KeyError as e:
                    debug.debug(debug.D_ERROR, '{} did not have a \'pearl_points\' attribute.'.format(mention.name))
                    debug.debug(debug.D_ERROR, e)
                finally:
                    debug.debug(debug.D_INFO, 'Giving {} a point.'.format(mention))
                    pearlpoints += 1
                    storage.set_user_attribute(message.guild.id, id, "pearl_points", pearlpoints)
                    p = storage.get_user_attribute(message.guild.id, id, "pearl_points")
                    debug.debug(debug.D_INFO, '{} has {} points now.'.format(mention, p))
                    response = strings.give_point(mention)
                    response = "{}||Alright, I gave a point to {}.".format(response, mention.mention)
                    if ptg - 1 == 1:
                        response = '{}||{}, you have {} point left to give.'.format(response, message.author.mention,
                                                                                      ptg - 1)
                    else:
                        response = '{}||{}, you have {} points left to give.'.format(response, message.author.mention,
                                                                                       ptg - 1)
                    storage.set_user_attribute(message.guild.id, message.author.id, 'available_pearl_points', ptg - 1)
                    return response
            else:
                return 'You don\'t have any more points to give today, {}.'.format(message.author.mention)
        else:
            response = 'I can\'t give a point to no one or myself.||'\
                'Try mentioning the person you want to give points to.'
    return response


def take_points(client, message):
    id = 'null'
    pearlpoints = 0
    response = '... nothing happened ...'
    if len(message.mentions) >= 3:
        return 'You can\'t take points from more than one person at a time.'
    for mention in message.mentions:
        if mention != client.user and mention != message.author and not mention.bot:
            ptg = 0
            try:
                ptg = storage.get_user_attribute(message.guild.id, message.author.id, 'available_pearl_points')
            except:
                pass
            if ptg > 0:
                id = mention.id

                try:
                    pearlpoints = int(storage.get_user_attribute(message.guild.id, id, "pearl_points"))
                except KeyError as e:
                    print('{} did not have a \'pearl_points\' attribute.'.format(mention))
                    print('{} was not given a point.'.format(mention))
                finally:
                    print('Taking a point from {}.'.format(mention))
                    pearlpoints -= 1
                    storage.set_user_attribute(message.guild.id, id, "pearl_points", pearlpoints)
                    p = storage.get_user_attribute(message.guild.id, id, "pearl_points")
                    print('{} has {} points now.'.format(mention, p))
                    response = strings.take_point(mention)
                    response = "{}||Alright, I took a point from {}.".format(response, mention.mention)
                    if ptg - 1 == 1:
                        response = '{}||{}, you have {} point left to take.'.format(response, message.author.mention,
                                                                                      ptg - 1)
                    else:
                        response = '{}||{}, you have {} points left to take.'.format(response, message.author.mention,
                                                                                       ptg - 1)
                    storage.set_user_attribute(message.guild.id, message.author.id, 'available_pearl_points', ptg - 1)
                    return response
            else:
                return 'You don\'t have any more points to take today, {}.'.format(message.author.mention)
        else:
            response = 'I can\'t take a point from no one or myself.||'\
                'Try mentioning the person you want to give points to.'
    return response


def read_points(client, message):
    id = 'null'
    pearlpoints = 0
    response = ''
    for mention in message.mentions:
        if mention != client.user:
            id = mention.id

            try:
                pearlpoints = int(storage.get_user_attribute(message.guild.id, id, "pearl_points"))
            except KeyError as e:
                debug.debug(debug.D_ERROR, '{} did not have a \'pearl_points\' attribute.'.format(mention))
                storage.set_user_attribute(message.guild.id, id, "pearl_points", pearlpoints)
                pearlpoints = int(storage.get_user_attribute(message.guild.id, id, "pearl_points"))
            finally:
                if pearlpoints == 1:
                    response = "{} has {} pearl point.".format(mention.mention, pearlpoints)
                else:
                    response = "{} has {} pearl points.".format(mention.mention, pearlpoints)
        return response


def reset_points(client, message):
    response = 'Pearl points for the following users have been reset:'
    if message.mention_everyone:
        users = storage.get_attribute_for_users(message.guild.id, "pearl_points")
        for i, u in enumerate(users):
            storage.remove_user_attribute(message.guild.id, u['id'], 'pearl_points')
            response = '{}||<@{}>'.format(response, u['id'])
    else:
        for mention in message.mentions:
            if mention != client.user:
                id = mention.id
                storage.remove_user_attribute(message.guild.id, id, "pearl_points")
                response = '{}||{}'.format(response, mention.mention)
    return response


def get_top_points(use_embed = False, raw = False):
    board = storage.get_attribute_for_users(private.tdt_server_id, "pearl_points")
    board = sorted(board, key = itemgetter('pearl_points'), reverse = True)

    if raw:
        return board
    elif not use_embed:
        response = 'Leaderboard:'
        for i, p in enumerate(board):
            response = '{0}\n{1}:[{2}] - <@{3}>'.format(response, i + 1, p['pearl_points'], p['id'])
            # response = '{0}||{1}:[{2}] - <@{3}>'.format(response, i + 1, p['pearl_points'], p['id'])
        return response
    elif use_embed:
        embed = discord.Embed(title = 'Leaderboard', color = misc.ANA_COLOR, footer='This is in beta testing.')
        # embed.set_author(name = 'Test Author Name')
        pos = ''
        pts = ''
        plr = ''
        for i, p in enumerate(board):
            pos = '{}{}\n'.format(pos, str(i + 1))
            pts = '{}{}\n'.format(pts, p['pearl_points'])
            plr = '{}<@{}>\n'.format(plr, p['id'])
        embed.add_field(name='#', value=pos, inline=True)
        embed.add_field(name='Pts', value=pts, inline=True)
        embed.add_field(name='User', value=plr, inline=True)
        return embed


def force_change_attribute(client, message, attribute_name, value):
    """Modifies the target users attribute by the given amount."""
    old_attribute = ''
    for mention in message.mentions:
        if mention != client.user:
            int_value = None
            try:
                old_attribute = storage.get_user_attribute(message.guild.id, mention.id, attribute_name)
            except KeyError as e:
                return '{} does not have a {} attribute.'.format(mention.mention, attribute_name)
            try:
                int_attribute = int(old_attribute)
            except ValueError as e:
                return 'Command is not valid on {} attribute'.format(attribute_name)
            try:
                int_value = int(value)
                storage.set_user_attribute(message.guild.id, mention.id, attribute_name, int_attribute + int_value)
                s = '{} attribute set to {}. (was {})'.format(attribute_name, int_attribute + int_value, int_attribute)
                return s
            except ValueError as e:
                return '{} is not a valid integer.'.format(value)
    return "I don't know what happened..."
