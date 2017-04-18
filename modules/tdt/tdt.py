import discord
import asyncio
import time
import random
import re

from modules.api import gw2
from modules.tdt import scoreboard
from modules.util import storage
from modules.util import debug
from datetime import datetime

anaeon_id = '108467075613216768'

server = discord.Object('108476397504217088')
channels = {
	'general' : '108476397504217088',
	'funny-stuff' : '108481880596197376',
	'bot-test-chat' : '231571819574984705'
	}

async def handleMessage(client, message):
	# maybe just reset the points here?
	# have it check the server attribute for when the next reset should be
	m = message.content.lower()
	try:
		if datetime.now() > storage.get_server_attribute(message.server.id, 'next_pearl_point_reset_datetime'):
			await client.send_message(message.channel, scoreboard.resetPointsToGive(message.server))
	except KeyError as e:
		debug.debug(debug.D_ERROR, e)
	debug.debug(debug.D_INFO, 'Time to next reset: {}'.format((storage.get_server_attribute(message.server.id, 'next_pearl_point_reset_datetime') - datetime.now())))
	# if it's past that time, reset.
	
	# respond to solo fractal emote and give daily fractals
	if m == '<:fractals:230520375396532224>':
		response = '```\nToday\'s daily fractals:\n\n'
		t = ''
		r = ''
		fractal_dailies = gw2.getFractalDailies()
		for daily in fractal_dailies:
			name = gw2.getAchievementName(daily['id'])
			if ' Tier ' in name and ' 4 ' in name:
				t = '{}{}\n'.format(t, gw2.getAchievementName(daily['id']))
			elif not ' Tier ' in name:
				r = '{}{}\n'.format(r, gw2.getAchievementName(daily['id']))
		await client.send_message(message.channel, '{}{}{}\n```'.format(response, r, t))
	
	# end fractals
	
	# Add reactions to some messages
	
	if 'treebs' in m or 'omega' in m:
		debug.debug(debug.D_INFO, 'Treebs was here...')
		await client.add_reaction(message, 'treebs:235655554465398784')
	
	# End adding reactions
	
	for mention in message.mentions: # when someone is mentioned
		debug.debug(debug.D_INFO, '{} was mentioned'.format(mention))
		if mention == client.user: # if the bot is mentioned
			response = ''
			
			# -- pearl points --
			
			if 'give' in m and ('pearlpoint' in m or 'pearl point' in m or ('pearl' in m and 'point' in m) or 'point' in m) and not '!resetpointstogive' in m:
				response = scoreboard.givePoints(client, message)
			elif ('take' in m or 'remove' in m) and ('pearlpoint' in m or 'pearl point' in m or ('pearl' in m and 'point' in m) or 'point' in m):
				response = scoreboard.takePoints(client, message)
			elif 'how many points' in m or 'how many pearlpoints' in m or ('how' in m and 'many' in m and 'points' in m):
				if ' i ' in m:
					debug.debug(debug.D_INFO, 'Fetching remaining points for {}.'.format(message.author))
					response = scoreboard.readPointsToGive(client, message)
				else:
					response = scoreboard.readPoints(client, message)
			elif 'who\'s winning' in m or'leaderboard' in m:
				response = scoreboard.getTopPoints()
			print('{}, {}'.format(message.author.id, anaeon_id))
			
			# -- end pearl points --
			
			# -- dailies --
			
			if re.search('\\bfractal(\\b|s)|\\bfric frac(\\b|s)', m):
				# if re.search('\\btoday\\b|\\bdaily\\b|\\bdailies\\b', m):
				response = '```\nToday\'s daily fractals:\n\n'
				t = ''
				r = ''
				fractal_dailies = gw2.getFractalDailies()
				for daily in fractal_dailies:
					name = gw2.getAchievementName(daily['id'])
					if ' Tier ' in name and ' 4 ' in name:
						t = '{}{}\n'.format(t, gw2.getAchievementName(daily['id']))
					elif not ' Tier ' in name:
						r = '{}{}\n'.format(r, gw2.getAchievementName(daily['id']))
				response = '{}{}{}\n```'.format(response, r, t)
			
			# -- dailies --
			
			# commands unique to myself
			if '!resetpearlpoints' in m and message.author.id == anaeon_id:
				response = scoreboard.resetPoints(client, message)
			if '!initpearlpoints' in m and message.author.id == anaeon_id:
				response = scoreboard.initPointsToGive(message)
			if '!resetpointstogive' in m and message.author.id == anaeon_id:
				response = scoreboard.resetPointsToGive(message.server)
			
			if response != '':
				await client.send_message(message.channel, response)