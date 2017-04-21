import requests
import json

fractal_names_by_scale = {
    '1': 'Urban Battleground',
    '2': 'Swampland',
    '3': 'Aquatic Ruins',
    '4': 'Uncategorized',
    '5': 'Snowblind',
    '6': 'Volcanic',
    '7': 'Cliffside',
    '8': 'Underground Facility',
    '9': 'Molten Furnace',
    '10': 'Molten Boss',
    '11': 'Urban Battleground',
    '12': 'Uncategorized',
    '13': 'Chaos',
    '14': 'Aetherblade',
    '15': 'Thaumanova Reactor',
    '16': 'Snowblind',
    '17': 'Underground Facility',
    '18': 'Captain Mai Trin Boss',
    '19': 'Volcanic',
    '20': 'Solid Ocean',
    '21': 'Swampland',
    '22': 'Cliffside',
    '23': 'Molten Furnace',
    '24': 'Aetherblade',
    '25': 'Nightmare',
    '26': 'Aquatic Ruins',
    '27': 'Snowblind',
    '28': 'Volcanic',
    '29': 'Underground Facility',
    '30': 'Chaos',
    '31': 'Urban Battleground',
    '32': 'Swampland',
    '33': 'Cliffside',
    '34': 'Thaumanova Reactor',
    '35': 'Solid Ocean',
    '36': 'Uncategorized',
    '37': 'Snowblind',
    '38': 'Chaos',
    '39': 'Molten Furnace',
    '40': 'Molten Boss',
    '41': 'Swampland',
    '42': 'Captain Mai Trin Boss',
    '43': 'Underground Facility',
    '44': 'Uncategorized',
    '45': 'Solid Ocean',
    '46': 'Volcanic',
    '47': 'Cliffside',
    '48': 'Thaumanova Reactor',
    '49': 'Aetherblade',
    '50': 'Nightmare',
    '51': 'Snowblind',
    '52': 'Volcanic',
    '53': 'Underground Facility',
    '54': 'Chaos',
    '55': 'Thaumanova Reactor',
    '56': 'Swampland',
    '57': 'Urban Battleground',
    '58': 'Molten Furnace',
    '59': 'Cliffside',
    '60': 'Solid Ocean',
    '61': 'Aquatic Ruins',
    '62': 'Uncategorized',
    '63': 'Chaos',
    '64': 'Thaumanova Reactor',
    '65': 'Aetherblade',
    '66': 'Urban Battleground',
    '67': 'Swampland',
    '68': 'Underground Facility',
    '69': 'Cliffside',
    '70': 'Molten Boss',
    '71': 'Aetherblade',
    '72': 'Volcanic',
    '73': 'Captain Mai Trin Boss',
    '74': 'Snowblind',
    '75': 'Nightmare',
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
    '87': 'Volcanic',
    '88': 'Chaos',
    '89': 'Swampland',
    '90': 'Molten Boss',
    '91': 'Uncategorized',
    '92': 'Volcanic',
    '93': 'Snowblind',
    '94': 'Cliffside',
    '95': 'Underground Facility',
    '96': 'Aetherblade',
    '97': 'Thaumanova Reactor',
    '98': 'Captain Mai Trin Boss',
    '99': 'Chaos',
    '100': 'Nightmare',
}


def get_fractal_dailies():
    req = requests.get('https://api.guildwars2.com/v2/achievements/daily')
    data = json.loads(req.content)
    fractal_dailies = data['fractals']
    return fractal_dailies


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

