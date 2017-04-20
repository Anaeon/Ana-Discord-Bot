import requests
import json


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
