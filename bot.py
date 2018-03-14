from discord.ext.commands import Bot
from MessageList import MessageList

client = Bot(command_prefix="§½~^¨¤")

async def send(channel, msg):
	#Get the messages to be sent as a list.
	messages = MessageList(msg)
	await messages.getMessageList()
	
	sentMessages = await messages.sendMessages(channel)
	
	return sentMessages