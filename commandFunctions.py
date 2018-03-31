from bot import send
from commandFunctionsRedirect import *
from fileIO import getLanguageText
from fileIO import loadPickle
from Permission import Permission
from PermissionChanger import PermissionChanger
from Prefix import Prefix
from StringHandler import StringHandler

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
	await message.saveUser()

async def settingsServerPermissionsGive(message, arguments):
	await changePermissions(message, arguments, "server", "allow")

async def settingsServerPermissionsDeny(message, arguments):
	await changePermissions(message, arguments, "server", "deny")

async def settingsServerPermissionsUndo(message, arguments):
	await changePermissions(message, arguments, "server", "undo")

async def settingsServerPermissionsClear(message, arguments):
	await clearPermissions(message, arguments, "server")

async def settingsChannelPermissionsGive(message, arguments):
	await changePermissions(message, arguments, "channel", "allow")

async def settingsChannelPermissionsDeny(message, arguments):
	await changePermissions(message, arguments, "channel", "deny")

async def settingsChannelPermissionsUndo(message, arguments):
	await changePermissions(message, arguments, "channel", "undo")

async def settingsChannelPermissionsClear(message, arguments):
	await clearPermissions(message, arguments, "channel")

async def infoPermissions(message, arguments):
	#Shows command permissions for all commands on this server, and all channel-specific permissions.
	
	language = await message.getLanguage()
	permissionDict = {}
	
	for channel in message.discord_py.server.channels:
		try:
			channelSettings = await loadPickle(channel.id, "savedData\\channels")
			await channelSettings.getPermissionsPerCommand(permissionDict, channel.id)
		except FileNotFoundError:
			pass
	
	await message.server_settings.getPermissionsPerCommand(permissionDict)
	print(permissionDict)
	
	stringHandler = StringHandler(dict=permissionDict)
	msgString = await stringHandler.getPermissionInfoText(message.discord_py, language)
	
	await send(message.discord_py.channel, msgString)

async def commandNotFound(message, command):
	msg = await getLanguageText(await message.getLanguage(), "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await send(message.discord_py.channel, msg)