import requests
import json

def getFractalDailies():
	req = requests.get('https://api.guildwars2.com/v2/achievements/daily')
	data = json.loads(req.content)
	fractal_dailies = data['fractals']
	return fractal_dailies
	
def getAchievementNames(id):
	names = []
	req = requests.get('https://api.guildwars2.com/v2/achievements?ids={}'.format(id))
	data = json.loads(req.content)
	for d in data:
		names.append(d['name'])
	return names