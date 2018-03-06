from discord.ext.commands import Bot

client = Bot(command_prefix="§½~^¨¤")

async def send(channel, msg):
	from MessageList import MessageList
	
	#Get the messages to be sent as a list.
	messages = MessageList(msg)
	await messages.getMessageList()
	
	sentMessages = await messages.sendMessages(channel)
	
	return sentMessages