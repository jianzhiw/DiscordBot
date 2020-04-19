# bot.py
import os
import logging
import discord
from dotenv import load_dotenv
import praw

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
			random = subreddit.random()
			#url = 'https://www.reddit.com{}'.format(random.permalink)
			#embed = discord.Embed(title = 'r/{}'.format(random.subreddit), url = url, type = 'rich')
			#embed.add_field(name=random.title, value=random.url, inline=False)
			subreddit_text = '**r/{}**'.format(random.subreddit)
			title = '**{}**'.format(random.title)
			await message.channel.send('{}\n{}\n{}'.format(subreddit_text, title, random.url))
			#await message.channel.send(embed=embed)
			logging.info('{} - {}'.format(message.author, message.content))
		except:
			await message.channel.send('Subreddit {} not found!'.format(message.content.split(' ',1)[1]))
			logging.info('Reddit exception: {} - {}'.format(message.author, message.content))

client.run(TOKEN)
