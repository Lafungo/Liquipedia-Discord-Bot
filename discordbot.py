# -*- coding: utf-8 -*-

# License MIT
# Copyright 2016-2017 Alex Winkler

import discord
import random
import requests
import json
import time

token = 'token'

client = discord.Client()

muted = False
game = discord.Game(name = 'Liquipedia', url = 'http://wiki.teamliquid.net', type = 1)

wikibaseurl = 'http://wiki.teamliquid.net/'
wikis = [
	'starcraft',
	'starcraft2',
	'dota2',
	'hearthstone',
	'heroes',
	'smash',
	'counterstrike',
	'overwatch',
	'commons',
	'warcraft',
	'fighters',
	'rocketleague',
	'clashroyale',
	'crossfire',
	'battlerite',
	'trackmania',
	'diabotical',
	'teamfortress',
	'leagueoflegends',
	'worldofwarcraft',
	'fifa',
	'pokemon',
	'quake',
	'rainbowsix',
	'pubg'
]
botroles = {
	'bw': 'Starcraft',
	'broodwar': 'Starcraft',
	'sc': 'Starcraft',
	'starcraft': 'Starcraft',
	'starcraftbroodwar': 'Starcraft',
	'sc2': 'Starcraft 2',
	'starcraft2': 'Starcraft 2',
	'starcraftii': 'Starcraft 2',
	'dota': 'Dota 2',
	'dota2': 'Dota 2',
	'hs': 'Hearthstone',
	'hearthstone': 'Hearthstone',
	'hots': 'Heroes',
	'heroes': 'Heroes',
	'heroesofthestorm': 'Heroes',
	'smash': 'Smash',
	'ssb': 'Smash',
	'ssbm': 'Smash',
	'melee': 'Smash',
	'sm4sh': 'Smash',
	'ssb4': 'Smash',
	'smash64': 'Smash',
	'projectm': 'Smash',
	'pm': 'Smash',
	'cs': 'Counter-Strike',
	'csgo': 'Counter-Strike',
	'counterstrike': 'Counter-Strike',
	'counterstrikeglobaloffensive': 'Counter-Strike',
	'counterstrike:globaloffensive': 'Counter-Strike',
	'ow': 'Overwatch',
	'overwatch': 'Overwatch',
	'commons': 'Commons',
	'war3': 'Warcraft',
	'wc3': 'Warcraft',
	'warcraft3': 'Warcraft',
	'warcraft': 'Warcraft',
	'fgc': 'Fighters',
	'fighters': 'Fighters',
	'streetfighter': 'Fighters',
	'sf': 'Fighters',
	'rl': 'Rocket League',
	'rocketleague': 'Rocket League',
	'clash': 'Clash Royale',
	'clashroyale': 'Clash Royale',
	'crossfire': 'CrossFire',
	'battlerite': 'Battlerite',
	'trackmania': 'TrackMania',
	'diabotical': 'Diabotical',
	'tf': 'Team Fortress',
	'tf2': 'Team Fortress',
	'teamfortress': 'Team Fortress',
	'teamfortress2': 'Team Fortress',
	'lol': 'League of Legends',
	'leagueoflegends': 'League of Legends',
	'wow': 'World of Warcraft',
	'worldofwarcraft': 'World of Warcraft',
	'pokemon': 'Pokémon',
	'pokémon': 'Pokémon',
	'quake': 'Quake',
	'fifa': 'FIFA',
	'r6': 'Rainbow Six',
	'r6s': 'Rainbow Six',
	'rainbow6': 'Rainbow Six',
	'rainbow6siege': 'Rainbow Six',
	'rainbowsix': 'Rainbow Six',
	'rainbowsixsiege': 'Rainbow Six',
	'pubg': 'PUBG'
}
sbotroles = {
	'randomstats': 'Random Stats of the Day',
	'randomstatsoftheday': 'Random Stats of the Day'
}
countchannelmessagemax = 100
countchannelmessage = {}
for wiki in wikis:
	countchannelmessage[wiki] = 0
lies = [
	'Liquipedia is not awesome... (good that this is a lie ^^)',
	'salle is a young girl',
	'Pizza is bad and no one likes it',
	'salle\'s ideas are always realistic',
	'Chrome is a decent browser',
	'blame swampflare',
	'The revision system of Liquipedia is useless, just kill the history',
	'I played Half Life 3 recently, it sucked',
	'WarCraft 4 is just about to be released',
	'Dota 2 is so tiny, we should focus on big esports like Nokia Snake instead',
	'https://files.catbox.moe/o8tify.gif',
]

def lie():
	global lies
	i = random.randrange(0, len(lies), 1)
	return lies[i]

def pendingchanges(wiki, displaynochanges):
	global wikibaseurl
	global wikis
	global countchannelmessage
	global countchannelmessagemax
	result = ''
	if wiki in wikis:
		if countchannelmessage[wiki] >= countchannelmessagemax or displaynochanges:
			countchannelmessage[wiki] = 0
			url = wikibaseurl + wiki + '/api.php?action=query&format=json&list=oldreviewedpages&ornamespace=0|10&orlimit=' + str(random.randrange(200, 500, 1))
			jsonobj = requests.get(url).json()
			results = jsonobj['query']['oldreviewedpages']
			count = len(results)
			if count == 0 and displaynochanges:
				result = 'No pending changes on ' + wiki
			elif count > 0:
				random.shuffle(results)
				plural = 's'
				if count == 1:
					plural = ''
				if count > 200:
					countstr = 'over 200'
				else:
					countstr = str(count)
				result = '**Pages with pending changes**: <' + wikibaseurl + wiki + '/Special:PendingChanges> (' + countstr + ' page' + plural + ' pending)'
				for i in range(0, min(count, 5)):
					result += '\n<' + wikibaseurl + wiki + '/' + results[i]['title'].replace(' ', '_') + '> (diff: ' + str(results[i]['diff_size']) + ', since: ' + results[i]['pending_since'][0:10] + ')'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def unreviewedpages(wiki, displaynochanges):
	global wikibaseurl
	global wikis
	global countchannelmessage
	global countchannelmessagemax
	result = ''
	if wiki in wikis:
		if countchannelmessage[wiki] >= countchannelmessagemax or displaynochanges:
			countchannelmessage[wiki] = 0
			url = wikibaseurl + wiki + '/api.php?action=query&format=json&list=unreviewedpages&urfilterredir=nonredirects&urnamespace=0|10&urlimit=' + str(random.randrange(200, 500, 1))
			jsonobj = requests.get(url).json()
			results = jsonobj['query']['unreviewedpages']
			count = len(results)
			if count == 0 and displaynochanges:
				result = 'No unreviewed pages on ' + wiki
			elif count > 0:
				random.shuffle(results)
				plural = 's'
				if count == 1:
					plural = ''
				if count > 200:
					countstr = 'over 200'
				else:
					countstr = str(count)
				result = '**Unreviewed pages**: <' + wikibaseurl + wiki + '/Special:UnreviewedPages> (' + countstr + ' page' + plural + ' unreviewed)'
				for i in range(0, min(count, 5)):
					result += '\n<' + wikibaseurl + wiki + '/' + results[i]['title'].replace(' ', '_') + '>'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def search(wiki, searchstring):
	global wikibaseurl
	global wikis
	global countchannelmessage
	global countchannelmessagemax
	result = ''
	if wiki in wikis:
		countchannelmessage[wiki] = 0
		url = wikibaseurl + wiki + '/api.php?action=query&format=json&list=search&srlimit=5&srsearch=' + searchstring
		jsonobj = requests.get(url).json()
		results = jsonobj['query']['search']
		count = jsonobj['query']['searchinfo']['totalhits']
		if count == 0:
			result = 'No results for **' + searchstring + '** on ' + wiki
		elif count > 0:
			plural = 's'
			if count == 1:
				plural = ''
			else:
				countstr = str(count)
			result = '**Search results**: <' + wikibaseurl + wiki + '/index.php?title=Special%3ASearch&profile=default&search=' + searchstring.replace(' ', '+') + '&fulltext=Search> (' + countstr + ' page' + plural + ')'
			for i in range(0, min(count, 5)):
				result += '\n<' + wikibaseurl + wiki + '/' + results[i]['title'].replace(' ', '_') + '>'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def die(sides): #My sides are killing me
	try:
		s = int(sides)
		if s > 0:
			result = 'Your ' + str(s) + '-sided die threw a ' + str(random.randrange(1, s + 1, 1)) + '.'
		else:
			result = 'Please use a positive whole number > 0.'
	except ValueError:
		result = 'Please use a positive whole number > 0.'
	return result

def dice(sides, count=1):
	try:
		s = int(sides)
		c = int(count)
		if s > 0:
			if c == 1:
				result = die(s)
			elif c > 1:
				rolls = [random.randrange(1, s + 1, 1) for _ in range(c)]
				result = 'Your ' + str(c) + ' ' + str(s) + '-sided dice threw ' + str(rolls) + ' for a total of ' + str(sum(rolls)) + '.'
			else:
				result = 'Please use two positive whole numbers > 0.'
		else:
			result = 'Please use two positive whole numbers > 0.'
	except ValueError:
		result = 'Please use two positive whole numbers > 0.'
	return result

@client.async_event
def on_ready():
	global game
	yield from client.change_status(game)

@client.async_event
def on_message(message):
	global muted
	global countchannelmessage
	global countchannelmessagemax
	global botroles
	global sbotroles
	global wikis
	if message.channel.name in wikis:
		countchannelmessage[message.channel.name] += 1
	if message.content == '!fobot' or message.content.startswith('!fobot'):
		if not muted:
			if message.content == '!fobot liquipedia':
				yield from client.send_message(message.channel, '**Liquipedia** is awesome! Use !fobot help to see the manual.')
			elif message.content == '!fobot guides':
				yield from client.send_message(message.channel, '**Liquipedia-Guides**: http://wiki.teamliquid.net/starcraft2/User:FO-BoT#Guides')
			elif message.content == '!fobot hype':
				yield from client.send_message(message.channel, '**\\\\Ü/ HYPE \\\\Ü/** http://stuff.gramma.name/hype/')
			elif message.content == '!fobot todo':
				yield from client.send_message(message.channel, '**Liquipedia-To Do Lists**: http://wiki.teamliquid.net/starcraft2/User:FO-BoT#To_Do_Lists')
			elif message.content == '!fobot dance':
				yield from client.send_message(message.channel, '**EVERYBODY DANCE \\\\Ü/**\n*dances :D\\\\-<*\n*dances :D|-<*\n*dances :D/-<*')
			elif message.content == '!fobot help':
				yield from client.send_message(message.channel, '**FO-BoT Commands**: http://wiki.teamliquid.net/starcraft2/User:FO-BoT#Manual')
			elif message.content == '!fobot lie':
				yield from client.send_message(message.channel, lie())
			elif message.content.startswith('!fobot talk ') and message.server == None and message.author.id == '138719439834185728':
				yield from client.send_message(message.channel, 'Hello ' + message.author.name)
			elif message.content == '!fobot coder':
				yield from client.send_message(message.channel, 'FO-BoT was coded by **FO-nTTaX**')
			elif message.content == '!fobot ranking':
				yield from client.send_message(message.channel, '**Liquipedia ranking**: http://wiki.teamliquid.net/statistics/')
			elif message.content == '!fobot thinking':
				yield from client.send_message(message.channel, 'https://files.catbox.moe/o8tify.gif')
			elif message.content == '!fobot lickypiddy':
				lickypiddywiki = 'commons'
				if message.channel.name in wikis:
					lickypiddywiki = message.channel.name
				else:
					lickypiddywiki = 'commons'
				yield from client.send_message(message.channel, 'http://wiki.teamliquid.net/' + lickypiddywiki + '/Special:Lickypiddy')
			elif message.content == '!fobot pendingchanges':
				result = pendingchanges(message.channel.name, True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot pendingchanges '):
				result = pendingchanges(message.content.replace('!fobot pendingchanges ', ''), True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content == '!fobot unreviewedpages':
				result = unreviewedpages(message.channel.name, True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot unreviewedpages '):
				result = unreviewedpages(message.content.replace('!fobot unreviewedpages ', ''), True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot search '):
				result = search(message.channel.name, message.content.replace('!fobot search ', ''))
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot die '):
				number = message.content.replace('!fobot die ', '')
				result = die(number)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot dice '):
				numbers = message.content.replace('!fobot dice ', '').split(' ')
				if len(numbers) == 1:
					result = die(numbers[0])
				elif len(numbers) == 2:
					result = dice(numbers[0], numbers[1])
				else:
					result = 'Please use two positive whole numbers > 0.'
				if result != '':
					yield from client.send_message(message.channel, result)
#			elif message.content.startswith('!fobot follow '):
#				yield from client.send_message(message.channel, 'TODO')
#			elif message.content.startswith('!fobot unfollow '):
#				yield from client.send_message(message.channel, 'TODO')
			elif message.content == '!fobot':
				yield from client.send_message(message.channel, '**Liquipedia** is awesome! Use !fobot help to see the manual.')
			elif message.content == '!fobot mute':
				muted = True
				yield from client.send_message(message.channel, '*Bot is muted now!*')
		if message.content == '!fobot unmute':
			muted = False
			yield from client.send_message(message.channel, '*Bot is unmuted now!*')
		elif message.content.startswith('!fobot addrole '):
			roleid = message.content.replace('!fobot addrole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in botroles:
				rolename = botroles[roleid]
				role = discord.utils.get(message.server.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					yield from client.add_roles(message.author, role)
					yield from client.send_message(message.channel, '**Success**: Role added')
				else:
					yield from client.send_message(message.channel, '**Error**: You can\'t add that role')
			else:
				yield from client.send_message(message.channel, '**Error**: You can\'t add that role')
		elif message.content.startswith('!fobot removerole '):
			roleid = message.content.replace('!fobot removerole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in botroles:
				rolename = botroles[roleid]
				role = discord.utils.get(message.server.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					yield from client.remove_roles(message.author, role)
					yield from client.send_message(message.channel, '**Success**: Role removed')
				else:
					yield from client.send_message(message.channel, '**Error**: You can\'t remove that role')
			else:
				yield from client.send_message(message.channel, '**Error**: You can\'t remove that role')
	elif message.content == '!sallebot' or message.content.startswith('!sallebot'):
		if message.content.startswith('!sallebot addrole '):
			roleid = message.content.replace('!sallebot addrole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in sbotroles:
				rolename = sbotroles[roleid]
				role = discord.utils.get(message.server.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					yield from client.add_roles(message.author, role)
					yield from client.send_message(message.channel, 'Since sallebot is lazy... I added the role for you :P')
				else:
					yield from client.send_message(message.channel, '**Error**: You can\'t add that role')
			else:
				yield from client.send_message(message.channel, '**Error**: You can\'t add that role')
		elif message.content.startswith('!sallebot removerole '):
			roleid = message.content.replace('!sallebot removerole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in sbotroles:
				rolename = sbotroles[roleid]
				role = discord.utils.get(message.server.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					yield from client.remove_roles(message.author, role)
					yield from client.send_message(message.channel, 'Since sallebot is lazy... I removed the role for you :P')
				else:
					yield from client.send_message(message.channel, '**Error**: You can\'t remove that role')
			else:
				yield from client.send_message(message.channel, '**Error**: You can\'t remove that role')
	if 'liquidpedia' in message.content.lower():
		yield from client.send_message(message.channel, 'It is **Liquipedia**, only one d in the name!')
	if message.channel.name in wikis:
		if countchannelmessage[message.channel.name] >= countchannelmessagemax:
			if message.channel.name != None:
				type = random.randrange(0, 2, 1)
				if type == 0:
					result = pendingchanges(message.channel.name, False)
					if result != '':
						yield from client.send_message(message.channel, result)
				elif type == 1:
					result = unreviewedpages(message.channel.name, False)
					if result != '':
						yield from client.send_message(message.channel, result)

client.run(token)
