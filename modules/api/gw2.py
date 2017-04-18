import requests
import json

def getFractalDailies():
	req = requests.get('https://api.guildwars2.com/v2/achievements/daily')
	data = json.loads(req.content)
	fractal_dailies = data['fractals']
	return fractal_dailies
	
def getAchievementName(id):
	name = 'Unknown achievement... ID == {}.'.format(id)
	req = requests.get('https://api.guildwars2.com/v2/achievements?ids={}'.format(id))
	data = json.loads(req.content)
	name = data[0]['name']
	return name