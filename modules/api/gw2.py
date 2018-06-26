import requests
import json
import discord

fractal_names_by_scale = {
    '1': 'Volcanic',
    '2': 'Uncategorized',
    '3': 'Snowblind',
    '4': 'Urban Battleground',
    '5': 'Swampland',
    '6': 'Cliffside',
    '7': 'Aquatic Ruins',
    '8': 'Underground Facility',
    '9': 'Molten Furnace',
    '10': 'Molten Boss',
    '11': 'Urban Battleground',
    '12': 'Uncategorized',
    '13': 'Chaos Isles',
    '14': 'Aetherblade',
    '15': 'Thaumanova Reactor',
    '16': 'Twilight Oasis',
    '17': 'Underground Facility',
    '18': 'Captain Mai Trin Boss',
    '19': 'Volcanic',
    '20': 'Solid Ocean',
    '21': 'Swampland',
    '22': 'Cliffside',
    '23': 'Molten Furnace',
    '24': 'Nightmare',
    '25': 'Shattered Observatory',
    '26': 'Aquatic Ruins',
    '27': 'Snowblind',
    '28': 'Volcanic',
    '29': 'Underground Facility',
    '30': 'Chaos Isles',
    '31': 'Urban Battleground',
    '32': 'Swampland',
    '33': 'Cliffside',
    '34': 'Thaumanova Reactor',
    '35': 'Solid Ocean',
    '36': 'Uncategorized',
    '37': 'Snowblind',
    '38': 'Chaos Isles',
    '39': 'Molten Furnace',
    '40': 'Molten Boss',
    '41': 'Twilight Oasis',
    '42': 'Captain Mai Trin Boss',
    '43': 'Underground Facility',
    '44': 'Uncategorized',
    '45': 'Solid Ocean',
    '46': 'Aetherblade',
    '47': 'Cliffside',
    '48': 'Thaumanova Reactor',
    '49': 'Nightmare',
    '50': 'Shattered Observatory',
    '51': 'Snowblind',
    '52': 'Volcanic',
    '53': 'Underground Facility',
    '54': 'Chaos Isles',
    '55': 'Thaumanova Reactor',
    '56': 'Swampland',
    '57': 'Urban Battleground',
    '58': 'Molten Furnace',
    '59': 'Twilight Oasis',
    '60': 'Solid Ocean',
    '61': 'Aquatic Ruins',
    '62': 'Uncategorized',
    '63': 'Chaos Isles',
    '64': 'Thaumanova Reactor',
    '65': 'Aetherblade',
    '66': 'Urban Battleground',
    '67': 'Swampland',
    '68': 'Snowblind',
    '69': 'Cliffside',
    '70': 'Molten Boss',
    '71': 'Aetherblade',
    '72': 'Volcanic',
    '73': 'Captain Mai Trin Boss',
    '74': 'Nightmare',
    '75': 'Shattered Observatory',
    '76': 'Aquatic Ruins',
    '77': 'Swampland',
    '78': 'Urban Battleground',
    '79': 'Uncategorized',
    '80': 'Solid Ocean',
    '81': 'Underground Facility',
    '82': 'Cliffside',
    '83': 'Molten Furnace',
    '84': 'Thaumanova Reactor',
    '85': 'Urban Battleground',
    '86': 'Snowblind',
    '87': 'Twilight Oasis',
    '88': 'Chaos Isles',
    '89': 'Swampland',
    '90': 'Molten Boss',
    '91': 'Uncategorized',
    '92': 'Volcanic',
    '93': 'Snowblind',
    '94': 'Cliffside',
    '95': 'Captain Mai Trin Boss',
    '96': 'Aetherblade',
    '97': 'Thaumanova Reactor',
    '98': 'Chaos Isles',
    '99': 'Nightmare',
    '100': 'Shattered Obsaervatory',
}


def get_fractal_dailies(get_as_embed = False):
    req = requests.get('https://api.guildwars2.com/v2/achievements/daily')
    data = json.loads(req.content)
    fractal_dailies = data['fractals']
    if not get_as_embed:
        return fractal_dailies
    else:
        embed = discord.Embed(title = 'Daily Fractals', color = int('ff0000', 16))
        return embed


def get_achievement_names(ids):
    names = []
    id_string = ''
    for ID in ids:
        id_string = '{}{},'.format(id_string, ID)
    req = requests.get('https://api.guildwars2.com/v2/achievements?ids={}'.format(id_string))
    data = json.loads(req.content)
    for d in data:
        names.append(d['name'])
    return names


def get_fractal_name(scale):
    return fractal_names_by_scale[scale]
