from bot import send
from commandFunctionsRedirect import *
from fileIO import getLanguageText
from fileIO import loadPickle
from Permission import Permission
from PermissionChanger import PermissionChanger
from Prefix import Prefix
from StringHandler import StringHandler

#Test command.
async def test(message, arguments):
	msg = await getLanguageText(message.language, "COMMAND.TEST.MESSAGE")
	await send(message.discord_py.channel, msg)

#Shows the prefixes.
async def prefixView(message, arguments):
	prefix = Prefix(message)
	msg = await prefix.getPrefixStrings()
	
	await send(message.discord_py.channel, msg)

#Changes the server prefix.
async def prefixServerChange(message, arguments):
	await message.server_settings.changePrefix(message, arguments)

#Clears the server prefix.
async def prefixServerClear(message, arguments):
	await message.server_settings.clearPrefix(message)

#Changes the channel prefix.
async def prefixChannelChange(message, arguments):
	await message.channel_settings.changePrefix(message, arguments)

#Clears the channel prefix.
async def prefixChannelClear(message, arguments):
	await message.channel_settings.clearPrefix(message)

#Changes the user prefix.
async def prefixUserChange(message, arguments):
	await message.user_settings.changePrefix(message, arguments)

#Clears the user prefix.
async def prefixUserClear(message, arguments):
	await message.user_settings.clearPrefix(message)

async def settingsServerPermissionsGive(message, arguments):
	await message.server_settings.changePermissions(message, arguments, "allow")

async def settingsServerPermissionsDeny(message, arguments):
	await message.server_settings.changePermissions(message, arguments, "deny")

async def settingsServerPermissionsUndo(message, arguments):
	await message.server_settings.changePermissions(message, arguments, "undo")

async def settingsServerPermissionsClear(message, arguments):
	await message.server_settings.clearPermissions(message, arguments)

async def settingsChannelPermissionsGive(message, arguments):
	await message.channel_settings.changePermissions(message, arguments, "allow")

async def settingsChannelPermissionsDeny(message, arguments):
	await message.channel_settings.changePermissions(message, arguments, "deny")

async def settingsChannelPermissionsUndo(message, arguments):
	await message.channel_settings.changePermissions(message, arguments, "undo")

async def settingsChannelPermissionsClear(message, arguments):
	await message.channel_settings.clearPermissions(message, arguments)

#Shows command permissions for all commands on this server, and all channel-specific permissions.
async def infoPermissions(message, arguments):
	permissionDict = {}
	
	for channel in message.discord_py.server.channels:
		try:
			channelSettings = await loadPickle(channel.id, "savedData\\channels")
			await channelSettings.getPermissionsPerCommand(permissionDict, channel.id)
		except FileNotFoundError:
			pass
	
	await message.server_settings.getPermissionsPerCommand(permissionDict)
	
	stringHandler = StringHandler(dict=permissionDict)
	msgString = await stringHandler.getPermissionInfoText(message.discord_py, message.language)
	
	await send(message.discord_py.channel, msgString)

async def serverLanguage(message, arguments):
	await message.server_settings.changeLanguage(message, arguments)

async def channelLanguage(message, arguments):
	await message.channel_settings.changeLanguage(message, arguments)

async def userLanguage(message, arguments):
	await message.user_settings.changeLanguage(message, arguments)

"""
async def commandNotFound(message, command):
	msg = await getLanguageText(message.language, "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await send(message.discord_py.channel, msg)
"""