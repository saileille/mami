import logging
from bot import client
from discord import Game
from fileIO import getBotToken
from fileIO import getCsvVar
from Message import Message

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="mami.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

@client.event
async def on_ready():
	defaultPrefix = await getCsvVar("DEFAULT_PREFIX", "basic", "staticData")
	await client.change_presence(
		game = Game(
			name = "{prefix}prefix.view to get started".format(prefix=defaultPrefix)
		)
	)
	
	print("Connected.")

@client.event
async def on_message(message):
	await handleMessage(message)

@client.event
async def on_message_edit(oldMsg, newMsg):
	if (oldMsg.content == newMsg.content):
		return
	
	await handleMessage(newMsg)

async def handleMessage(discordMessage):
	#Mami does not have to deal with bots.
	if (discordMessage.author.bot == True):
		return
	
	message = Message(discordMessage)
	await message.getSettings()
	
	if (message.server_settings != None):
		print("\nSERVER")
		for key in message.server_settings.permissions:
			print(key)
			print(message.server_settings.permissions[key].__dict__)
	
	print("\nCHANNEL")
	for key in message.channel_settings.permissions:
		print(key)
		print(message.channel_settings.permissions[key].__dict__)
	
	#Processes text and executes commands.
	await message.separate()
	await message.executeCommands()

client.run(getBotToken())