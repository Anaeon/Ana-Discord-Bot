import requests
import json

def getFractalDailies():
	req = requests.get('https://api.guildwars2.com/v2/achievements/daily')
	data = json.loads(req.content)
	fractal_dailies = data['fractals']
	return fractal_dailies
	
def getAchievementNames(ids):
	names = []
	id_string = ''
	for id in ids:
		id_string = '{}{},'.format(id_string, id)
	req = requests.get('https://api.guildwars2.com/v2/achievements?ids={}'.format(id_string))
	data = json.loads(req.content)
	for d in data:
		names.append(d['name'])
	return names