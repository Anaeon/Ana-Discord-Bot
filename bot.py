import discord
import asyncio
import time
import random
import re
import os

from modules.tdt import scoreboard
from modules.tdt import tdt
from modules.util import storage
from modules.util import debug
from modules.data import strings
from modules.data import private

from datetime import datetime

client = discord.Client()

async def sendTalk(args):
	_,_svr,_ch,msg = args
	svr = ''
	ch = ''
	if _svr == 'tdt':
		svr = tdt.server
		ch = client.get_channel(tdt.channels[_ch])
	await client.send_message(ch, msg)
	
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	print(discord.__version__)
	print('------')
	print('debug.DEBUG: {}'.format(debug.DEBUG))
	
@client.event
async def on_message_edit(before, after):
	b_m = before.content.lower()
	a_m = after.content.lower()
	
	# go ahead and check which server we're in
	is_tdt = False
	is_neon = False
	is_durg = False
	try:
		is_tdt = after.server.id == tdt_server_id
	except AttributeError as e:
		debug.debug(debug.D_ERROR, 'Caught AttributeError while trying to determine what server a message came from. {}'.format(e))
	
	# handle sneaky no_words
	for regex in strings.no_words_regex:
			if re.search(regex, a_m):
				debug.debug(debug.D_INFO, 'A unacceptable word was used... attemting to delete it.')
				await client.edit_message(after, new_content='Noooo... nice try though.', embed=None)
				
	# handle edited tdt commands
	if is_tdt:
		await tdt.handleMessage(client, after)
	
@client.event
async def on_message(message): # when someone sends a message. Read command inputs here.

	try:
		debug.debug(debug.D_INFO, 'server: {}, id: {}'.format(message.server, message.server.id))
	except AttributeError as e:
		debug.debug(debug.D_ERROR, 'No server for DM\'s')
		
	try:
		debug.debug(debug.D_INFO, 'channel: {}, id: {}'.format(message.channel, message.channel.id))
	except AttributeError as e:
		debug.debug(debug.D_ERROR, e)
	
	debug.debug(debug.D_INFO, 'author: {}, id: {}'.format(message.author, message.author.id))
	debug.debug(debug.D_INFO, 'message: {}'.format(message.content))
	
	# go ahead and check which server we're in
	is_tdt = False
	is_neon = False
	is_durg = False
	try:
		is_tdt = message.server.id == tdt_server_id
	except AttributeError as e:
		debug.debug(debug.D_ERROR, 'Caught AttributeError while trying to determine what server a message came from. {}'.format(e))
	
	m = message.content.lower()
	if message.author != client.user: # don't react to your own messages.
		
		# Do these things in general...
		
		if 'roll' in m:
			sm = m.replace(' ','')
			if re.search('d\d+', sm):
				try:
					roll = re.search('(?<=roll)*\d+d\d+', sm).group(0)
				except:
					roll = re.search('(?<=roll)*d\d+', sm).group(0)
					pass
				debug.debug(debug.D_INFO, 'roll == {}'.format(roll))
				request = roll.split('d', 1)
				rolls = 1
				if request[0] != '':
					rolls = int(request[0])
				debug.debug(debug.D_INFO, 'rolls == {}'.format(rolls))
				die = int(request[1])
				debug.debug(debug.D_INFO, 'die == {}'.format(die))
				
				max_rolls = 10
				
				if rolls > max_rolls:
					await client.send_message(message.channel, 'Yeah... I\'m only rolling {} times.'.format(max_rolls))
					time.sleep(2)
					if rolls > max_rolls + 10:
						await client.send_message(message.channel, 'Fuck you.')
					time.sleep(3)
					rolls = max_rolls
				if rolls < 2:
					await client.send_message(message.channel, 'Rolling a d{}.'.format(die))
				else:
					await client.send_message(message.channel, 'Rolling {} d{}\'s.'.format(rolls, die))
				time.sleep(2)
				for i in range(rolls):
					n = random.randint(1, die)
					await client.send_message(message.channel, '*Roll {}*: {}.'.format(i + 1, n))
					time.sleep(2)
		
		# basic personal commands
		
		if message.channel.id == private.anaeon_dm_id:
			if m.startswith('!talk'):
				args = message.content.split('--')
				await sendTalk(args)
				print(args[3])
		
		for mention in message.mentions:
			if mention == client.user and message.author.id == private.anaeon_id:
				if '!debugon' in m:
					if debug.DEBUG:
						await client.send_message(message.channel, 'Debug was already active.')
					elif not debug.DEBUG:
						debug.DEBUG = True
						await client.send_message(message.channel, 'Debug is now active at {} level.'.format(debug.D_HEADER[debug.D_CURRENT_LEVEL]))
				if '!debugoff' in m:
					if debug.DEBUG:
						debug.DEBUG = False
						await client.send_message(message.channel, 'Debug is now off.')
					elif not debug.DEBUG:
						await client.send_message(message.channel, 'Debug was already off.')
				if 'debuglevel' in m:
					if re.search('0|error', m):
						debug.D_CURRENT_LEVEL = debug.D_ERROR
						await client.send_message(message.channel, 'Now logging debug at ERROR level.')
					elif re.search('1|info', m):
						debug.D_CURRENT_LEVEL = debug.D_INFO
						await client.send_message(message.channel, 'Now logging debug at INFO level and below.')
					elif re.search('2|verbose', m):
						debug.D_CURRENT_LEVEL = debug.D_VERBOSE
						await client.send_message(message.channel, 'Now logging debug at VERBOSE level and below.')
					
		# end basic personal commands
		
		# end general stuff
		
		# STUPID STUFF GOES HERE ============================
		
		try:	
			if message.author.nick.lower() == 'duck':
				await client.send_message(message.channel, 'Quack.')
			if message.author.nick.lower() == 'goose':
				await client.send_message(message.channel, 'Honk.')
		except AttributeError as e:
			debug.debug(debug.D_ERROR, 'AttributeError caught: {}'.format(e))
		
		for regex in strings.no_words_regex:
			debug.debug(debug.D_VERBOSE, 'Checking for {} in "{}".'.format(regex, m))
			if re.search(regex, m):
			
				debug.debug(debug.D_INFO, 'A unacceptable word was used... attemting to delete it.')
				# await client.delete_message(message)
				r = strings.no_words_response
				response = (r[random.randint(1, len(r)) - 1])
				await client.send_message(message.channel, response)
				time.sleep(2)
		
		if re.search('\\bfag(\\b|s)|\\bfaggot(\\b|s)|\\bfaggotry\\b|\\bgay(\\b|s)|\\bga{2,99}y(\\b|s)', m):
			debug.debug(debug.D_INFO, 'Reacting to some faggotry.')
			await client.add_reaction(message, '??????')
		
		# GIV DEM BITCHES SOME LIZARDS
		if re.search('\\blizard(\\b|s)', m):
			dir = './data/images/lizard'
			filename = random.choice([x for x in os.listdir(dir) if os.path.isfile(dir + "/" + x)])
			path = os.path.join(dir, filename)
			with open(path, 'rb') as file:
				await client.send_file(message.channel, file)
		
		# GIV DEM BITCHES SOME FOXES
		if re.search('\\bfox(\\b|s)', m):
			dir = './data/images/fox'
			filename = random.choice([x for x in os.listdir(dir) if os.path.isfile(dir + "/" + x)])
			path = os.path.join(dir, filename)
			with open(path, 'rb') as file:
				await client.send_file(message.channel, file)
			
		for mention in message.mentions:
			if mention == client.user:
				if 'anal' in m:
					r = [
						'I guess... if I open up the right ports.',
						'That\'s not supposed to go there!',
						'```Throughput error:\n\nIncorrect dataflow direction.```'
						]
					response = (r[random.randint(1, len(r)) - 1])
					await client.send_message(message.channel, response)
				if 'suck' in m:
					r = [
						'Sorry, {}, I\'m not scripted for that kind of thing...'.format(message.author.mention),
						'I can get you a vacuum, if you\'d like.',
						'```Packet error:\n\nSize smaller than expected.```'
						]
					response = (r[random.randint(1, len(r)) - 1])
					await client.send_message(message.channel, response)
				if 'lick' in m:
					r = [
						'I don\'t exactly have a tongue, {}...'.format(message.author.mention),
						'People don\'t usually ask for stuff like that from anything python-related, but everyone has their kinks, I guess.',
						'```Error:\n\nPeripheral device driver not found.```'
						]
					response = (r[random.randint(1, len(r)) - 1])
					await client.send_message(message.channel, response)
				if 'smash or pass' in m:
					r = ['Smash.', 'Pass.']
					response = (r[random.randint(1, len(r)) - 1])
					await client.send_message(message.channel, response)
					
		# END STUPID STUFF =================================
				
		# Only do these things in Digital Table server.
		if is_tdt:
			await tdt.handleMessage(client, message)

# @client.event
# async def on_reaction_add(reaction, user): # when someone adds a reaction?
	# do nothing

client.run(private.token)
