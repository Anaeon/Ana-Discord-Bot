import random

from operator import itemgetter
from datetime import datetime

from modules.data import strings
from modules.util import storage
from modules.util import debug

dailyPoints = 1
pointToGiveCap = 3


def init_points_to_give(message):
    users = message.server.members
    response = 'The following users have been initialized, and have one point to give:\n\n'
    for user in users:
        try:
            storage.get_user_attribute(user.id, 'available_pearl_points')
        except KeyError as e:
            storage.set_user_attribute(user.id, 'available_pearl_points', dailyPoints)
            response = '{}{}'.format(response, user.mention)

    # also init the server attribute for the datetime of the next reset
    x = datetime.today()  # today
    y = x.replace(day = x.day + 1, hour = 17, minute = 0, second = 0, microsecond = 0)  # tomorrow at 5

    delta_t = y - x  # time between now and next reset
    secs = delta_t.seconds + 1

    storage.set_server_attribute(message.server.id, 'next_pearl_point_reset_datetime', y)
    return response


def reset_points_to_give(server):
    users = server.members
    response = 'The following users have been given new points to use:\n\n'
    for user in users:
        user_points_left = 0
        try:
            user_points_left = storage.get_user_attribute(user.id, 'available_pearl_points')
            if user_points_left < pointToGiveCap:
                give = user_points_left + dailyPoints
                storage.set_user_attribute(user.id, 'available_pearl_points', give)
                response = '{}{}\n'.format(response, user.mention)
        except KeyError as e:
            pass

    # await client.send_message(server, response)
    debug.debug(debug.D_INFO, 'Points to spend have been reset')
    x = datetime.today()  # today
    if datetime.now().hour < 17:
        y = x.replace(hour = 17, minute = 0, second = 0, microsecond = 0)  # today at 5
    else:
        y = x.replace(day = x.day + 1, hour = 17, minute = 0, second = 0, microsecond = 0)  # tomorrow at 5

    delta_t = y - x  # time between now and next reset
    secs = delta_t.seconds + 1

    # t = Timer(secs, resetPointsToGive(server))

    storage.set_server_attribute(server.id, 'next_pearl_point_reset_datetime', y)
    return response


def read_points_to_give(client, message):
    id = 'null'
    pearlpointstogive = 0
    response = '... nothing happened ...'
    for mention in message.mentions:
        id = message.author.id

        try:
            pearlpointstogive = int(storage.get_user_attribute(id, 'available_pearl_points'))
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
        if mention != client.user and mention != message.author and not mention.bot:
            ptg = 0
            try:
                ptg = storage.get_user_attribute(message.author.id, 'available_pearl_points')
            except:
                pass
            if ptg > 0:
                id = mention.id
                try:
                    pearlpoints = int(storage.get_user_attribute(id, "pearl_points"))
                except KeyError as e:
                    debug.debug(debug.D_ERROR, '{} did not have a \'pearl_points\' attribute.'.format(mention))
                    debug.debug(debug.D_ERROR, e)
                finally:
                    debug.debug(debug.D_INFO, 'Giving {} a point.'.format(mention))
                    pearlpoints += 1
                    storage.set_user_attribute(id, "pearl_points", pearlpoints)
                    p = storage.get_user_attribute(id, "pearl_points")
                    debug.debug(debug.D_INFO, '{} has {} points now.'.format(mention, p))

                    give_point = [
                        "{}, you did a thing!".format(mention.mention),
                        "Yay!",
                        "Congrats, {}, you dirty bastard.".format(mention.mention),
                        "Did you really earn that point?",
                        "Congratulations.",
                        "{}, your friends have acknowledged your existance.".format(mention.mention),
                        "Fine... I guess.",
                        "Alright, but I don't like it.",
                        "Are you sure? Like... really sure?\n\nOoookkkkkk.",
                        "Finally! 'Bout time.",
                        "Do I even want to know what you had to do to get that, {}?".format(mention.mention),
                        "Don't spend it all in one place. ;D",
                        "Woooooow hooow speciaaaallll. *rolls eyes*",
                        "Hurray!"
                    ]

                    response = random.choice(give_point)
                    response = "{}\n\nAlright, I gave a point to {}.".format(response, mention.mention)
                    if ptg - 1 == 1:
                        response = '{}\n\n{}, you have {} point left to give.'.format(response, message.author.mention,
                                                                                      ptg - 1)
                    else:
                        response = '{}\n\n{}, you have {} points left to give.'.format(response, message.author.mention,
                                                                                       ptg - 1)
                    storage.set_user_attribute(message.author.id, 'available_pearl_points', ptg - 1)
            else:
                response = 'You don\'t have any more points to give today, {}.'.format(message.author.mention)
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
                ptg = storage.get_user_attribute(message.author.id, 'available_pearl_points')
            except:
                pass
            if ptg > 0:
                id = mention.id

                try:
                    pearlpoints = int(storage.get_user_attribute(id, "pearl_points"))
                except KeyError as e:
                    print('{} did not have a \'pearl_points\' attribute.'.format(mention))
                    print('{} was not given a point.'.format(mention))
                finally:
                    print('Taking a point from {}.'.format(mention))
                    pearlpoints -= 1
                    storage.set_user_attribute(id, "pearl_points", pearlpoints)
                    p = storage.get_user_attribute(id, "pearl_points")
                    print('{} has {} points now.'.format(mention, p))

                    take_point = [
                        "LOL!",
                        "Ha! Loser.",
                        "Get owned!",
                        "Say, \"Bye bye,\" point.",
                        "Oooooh~ You're in troubleeee~",
                        "You dun fucked up!",
                        "What did you do now, {}?".format(mention.mention),
                        "Your friends have deemed you an awful person, {}.".format(mention.mention),
                        "Your friends have denied you any glory or honor, {}.".format(mention.mention),
                        "git gud",
                        "RIP",
                        "GG EZ",
                        "Sucks to suck.",
                        "Adiós, punto.",
                        "Say, \"Goodbye,\" to your likeability, {}.".format(mention.mention)
                    ]

                    response = (take_point[random.randint(1, len(take_point)) - 1])
                    response = "{}\n\nAlright, I took a point from {}.".format(response, mention.mention)
                    if ptg - 1 == 1:
                        response = '{}\n\n{}, you have {} point left to take.'.format(response, message.author.mention,
                                                                                      ptg - 1)
                    else:
                        response = '{}\n\n{}, you have {} points left to take.'.format(response, message.author.mention,
                                                                                       ptg - 1)
                    storage.set_user_attribute(message.author.id, 'available_pearl_points', ptg - 1)
            else:
                response = 'You don\'t have any more points to take today, {}.'.format(message.author.mention)
    return response


def read_points(client, message):
    id = 'null'
    pearlpoints = 0
    for mention in message.mentions:
        if mention != client.user:
            id = mention.id
            response = ''
            try:
                pearlpoints = int(storage.get_user_attribute(id, "pearl_points"))
            except KeyError as e:
                debug.debug(debug.D_ERROR, '{} did not have a \'pearl_points\' attribute.'.format(mention))
                storage.set_user_attribute(id, "pearl_points", pearlpoints)
            finally:
                if pearlpoints == 1:
                    response = "{} has {} pearl point.".format(mention.mention, pearlpoints)
                else:
                    response = "{} has {} pearl points.".format(mention.mention, pearlpoints)
        return response


def reset_points(client, message):
    response = 'Pearl points for the following users have been reset: \n\n'
    if message.mention_everyone:
        users = storage.get_attribute_for_users("pearl_points")
        for i, u in enumerate(users):
            storage.remove_user_attribute(u['id'], 'pearl_points')
            response = '{}<@{}>\n'.format(response, u['id'])
    else:
        for mention in message.mentions:
            if mention != client.user:
                id = mention.id
                storage.remove_user_attribute(id, "pearl_points")
                response = '{}{}\n'.format(response, mention.mention)
    return response


def get_top_points():
    board = storage.get_attribute_for_users("pearl_points")
    board = sorted(board, key = itemgetter('pearl_points'), reverse = True)
    response = 'Leaderboard:\n\n'
    for i, p in enumerate(board):
        response = '{0}{1}:[{2}] - <@{3}>\n'.format(response, i + 1, p['pearl_points'], p['id'])
    return response
