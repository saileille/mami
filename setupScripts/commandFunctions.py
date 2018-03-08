async def test(message, arguments):
	#Test command.
	from fileIO import getLanguageText
	from bot import send
	
	msg = await getLanguageText(message.language, "COMMAND.TEST.MESSAGE")
	await send(message.discord_py.channel, msg)

async def prefixView(message, arguments):
	#Shows the prefixes.
	from bot import send
	from Prefix import Prefix
	
	prefix = Prefix(message)
	msg = await prefix.getPrefixStrings()
	
	await send(message.discord_py.channel, msg)

async def prefixUser(message, arguments):
	#Changes the user prefix.
	pass

async def commandNotFound(message, command):
	from fileIO import getLanguageText
	from bot import send
	
	msg = await getLanguageText(message.language, "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await send(message.discord_py.channel, msg)