async def commandHandler(commandCall, message):
	#This function takes the command code as a string and passes it on to the appropriate function.
	from fileIO import getLanguageVar
	
	#Command string is saved so that commandNotFound can access what was originally typed.
	commandStr = commandCall.commands[0]
	command = await getLanguageVar(message.server_settings.language, commandStr)
	
	if (command == "COMMAND.TEST.NAME"):
		await eval("await test(message)")
	
	else:
		await commandNotFound(message, commandStr)

async def test(message):
	from fileIO import getLanguageText
	from bot import client
	
	msg = await getLanguageText(message.server_settings.language, "COMMAND.TEST.MESSAGE")
	await client.send_message(message.discord_py.channel, msg)

async def commandNotFound(message, command):
	from fileIO import getLanguageText
	from bot import client
	
	msg = await getLanguageText(message.server_settings.language, "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await client.send_message(message.discord_py.channel, msg)