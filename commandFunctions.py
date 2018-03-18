from bot import send
from commandFunctionsRedirect import *
from fileIO import getLanguageText
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
	#Shows command permissions in both server and channel.
	language = await message.getLanguage()
	permissionChanger = PermissionChanger(arguments, language, "clear")
	await permissionChanger.parseCommands()
	
	if (permissionChanger.valid_change == False):
		return
	
	msgList = []
	for i in range(len(permissionChanger.command_codes)):
		code = permissionChanger.command_codes[i]
		msgList.append("**" + permissionChanger.command_strings[i] + "**")
		
		permissionType = await getLanguageText(language, "SERVER")
		msgList.append("*" + permissionType + "*")
		
		serverPermission = await permissionChanger.getPermissionObject(code, message.server_settings.permissions)
		msgList += await serverPermission.getPermissionString(message.discord_py, language)
		
		permissionType = await getLanguageText(language, "CHANNEL")
		msgList.append("*" + permissionType + "*")
		
		channelPermission = await permissionChanger.getPermissionObject(code, message.channel_settings.permissions)
		msgList += await channelPermission.getPermissionString(message.discord_py, language)
	
	msg = await StringHandler(list=msgList).getChapterDivide()
	await send(message.discord_py.channel, msg)

async def commandNotFound(message, command):
	msg = await getLanguageText(await message.getLanguage(), "COMMAND.NOT_FOUND")
	msg = msg.format(commandName=command)
	
	await send(message.discord_py.channel, msg)