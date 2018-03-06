async def test(message):
	from fileIO import getLanguageText
	from bot import send
	
	msg = await getLanguageText(message.server_settings.language, "COMMAND.TEST.MESSAGE")
	await send(message.discord_py.channel, msg)

async def commandNotFound(message, command):
	from fileIO import getLanguageText
	from bot import send
	
	msg = await getLanguageText(message.server_settings.language, "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await send(message.discord_py.channel, msg)