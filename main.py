from bot import client
import logging
from secrets import BOT_TOKEN
#import os

#FILE_DIRECTORY = os.getcwd()
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="mami.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

@client.event
async def on_ready():
	from fileIO import getCsvVar
	from discord import Game
	
	defaultPrefix = await getCsvVar("DEFAULT_PREFIX", "basic", "staticData")
	await client.change_presence(
		game = Game(
			name = "{prefix}help | {prefix}invite".format(prefix=defaultPrefix)
		)
	)
	
	print("Connected.")
	
	#For testing: uncomment for the window to remain.
	#input()

@client.event
async def on_message(discordMessage):
	from Message import Message
	from User import User
	from Server import Server
	from fileIO import loadPickle
	from fileIO import getCsvVar
	
	#Mami does not have to deal with bots.
	if (discordMessage.author.bot == True):
		return
	
	message = Message(discordMessage)
	await message.getSettings()
	
	#Processes text and executes commands.
	await message.separate()
	await message.executeCommands()

client.run(BOT_TOKEN)