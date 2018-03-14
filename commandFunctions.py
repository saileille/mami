from bot import send
from fileIO import getLanguageText
from PermissionChanger import PermissionChanger
from Prefix import Prefix

async def test(message, arguments):
	#Test command.
	
	msg = await getLanguageText(await message.getLanguage(), "COMMAND.TEST.MESSAGE")
	await send(message.discord_py.channel, msg)

async def prefixView(message, arguments):
	#Shows the prefixes.
	prefix = Prefix(message)
	msg = await prefix.getPrefixStrings()
	
	await send(message.discord_py.channel, msg)

async def prefixUser(message, arguments):
	#Changes the user prefix.
	newPrefix = " ".join(arguments)
	
	await message.user_settings.changePrefix(message, newPrefix)
	await message.user_settings.save(message.discord_py)

async def settingsServerPermissionsGive(message, arguments):
	permissionChanger = PermissionChanger(arguments)
	success = await permissionChanger.changePermissions(message.server_settings, await message.getLanguage(), type="allow")
	
	if (success == False):
		return
	
	await message.server_settings.save(message.discord_py)
	await send(message.discord_py.channel, "Succ")

async def settingsServerPermissionsDeny(message, arguments):
	permissionChanger = PermissionChanger(arguments)
	success = await permissionChanger.changePermissions(message.server_settings, await message.getLanguage(), type="deny")
	
	if (success == False):
		return
	
	await message.server_settings.save(message.discord_py)
	await send(message.discord_py.channel, "Succ")

async def settingsServerPermissionsUndo(message, arguments):
	permissionChanger = PermissionChanger(arguments)
	success = await permissionChanger.changePermissions(message.server_settings, await message.getLanguage(), type="undo")
	
	if (success == False):
		return
	
	await message.server_settings.save(message.discord_py)
	await send(message.discord_py.channel, "Succ")

async def commandNotFound(message, command):
	msg = await getLanguageText(await message.getLanguage(), "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await send(message.discord_py.channel, msg)