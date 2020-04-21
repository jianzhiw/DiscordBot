# bot.py
import os
import logging
import discord
from dotenv import load_dotenv
import praw
import urllib
import json
import random
import requests

#Create Logs
logFile = 'discord-bot.log'
logging.basicConfig(
	filename=logFile,
	filemode='a',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s: %(message)s',
	datefmt='%Y-%m-%dT%H:%M:%S'
)

load_dotenv()
#Reddit
reddit = praw.Reddit(
	client_id=os.getenv('REDDIT_CLIENT_ID'),
	client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
	user_agent=os.getenv('REDDIT_USER_AGENT'),
	username=os.getenv('REDDIT_USERNAME'),
	password=os.getenv('REDDIT_PASSWORD')
)

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GIPHY = os.getenv('GIPHY_API')

with_recp = ['back', 'bday', 'blackadder', 'bm', 'bus', 
            'chainsaw', 'cocksplat', 'ffs', 'ing', 
            'gfy', 'keep', 'king', 'legend', 'linus', 
            'madison', 'nugget', 'off', 'outside', 
            'problem', 'shakespeare', 'shutup', 
            'think', 'thinking', 'thumbs', 'waste', 'you']
without_recp = ['asshole', 'bag', 'because', 'bucket', 
               'bye', 'cup', 'diabetes', 'even', 'flying', 
               'ftfy', 'fyyff', 'give', 'horse', 'life', 
               'looking', 'me', 'no', 'programmer', 
               'question', 'ratsarse', 'retard', 'sake', 
               'shit', 'that', 'what', 'zero']

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    logging.info('{} connected to {}'.format(client.user, guild.name))

    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
	if message.content.upper() == '!TEST':
		await message.channel.send('Test Complete!')
		logging.info('{} - {}'.format(message.author, message.content))
	elif message.content.upper()[:7] == '!REDDIT':
		try:
			subreddit = reddit.subreddit(message.content.split(' ', 1)[1])
			#url = 'https://www.reddit.com{}'.format(subreddit.random().permalink)
			#url = subreddit.random().url
			subreddit_random = subreddit.random()
			#url = 'https://www.reddit.com{}'.format(random.permalink)
			#embed = discord.Embed(title = 'r/{}'.format(random.subreddit), url = url, type = 'rich')
			#embed.add_field(name=random.title, value=random.url, inline=False)
			subreddit_text = '**r/{}**'.format(subreddit_random.subreddit)
			title = '**{}**'.format(subreddit_random.title)
			await message.channel.send('{}\n{}\n{}'.format(subreddit_text, title, subreddit_random.url))
			#await message.channel.send(embed=embed)
			logging.info('{} - {}'.format(message.author, message.content))
		except:
			await message.channel.send('Subreddit {} not found!'.format(message.content.split(' ',1)[1]))
			logging.info('Reddit exception: {} - {}'.format(message.author, message.content))
	elif message.content.upper()[:4] == '!GIF':
		tag = message.content.split(' ', 1)[1].replace(' ', '%20')
		url = 'https://api.giphy.com/v1/gifs/random?api_key={}&tag={}&rating=R'.format(GIPHY, tag)
		data = json.load(urllib.request.urlopen(url))
		gif = data['data']['url']
		await message.channel.send(gif)
		logging.info('{} - {}'.format(message.author, message.content))
	elif message.content.upper()[:7] == '!INSULT':
		header = {'Accept': 'text/plain'}
		if len(message.content.split(' ')) == 1:
			url = 'https://www.foaas.com/{}/<@!{}>'.format(random.choice(without_recp), message.author.id)
			data = requests.get(url, headers=header)
			await message.channel.send(data.text)
		elif len(message.content.split(' ')) == 2:
			url = 'https://www.foaas.com/{}/{}/<@!{}>'.format(random.choice(with_recp), message.content.split(' ')[1], message.author.id)
			data = requests.get(url, headers=header)
			await message.channel.send(data.text)
		else:
			await message.channel.send('`!Insult` only accept maximum one parameter!')

		logging.info('{} - {}'.format(message.author, message.content))
client.run(TOKEN)
