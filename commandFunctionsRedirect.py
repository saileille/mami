from bot import send
from fileIO import getLanguageText
from PermissionChanger import PermissionChanger

#Some very similar command functions get redirected here.

async def changePermissions(message, arguments, settingsType, operation):
	language = await message.getLanguage()
	
	if (settingsType == "server"):
		settingObject = message.server_settings
	else:
		settingObject = message.channel_settings
	
	permissionChanger = PermissionChanger(arguments, language, operation)
	await permissionChanger.changePermissions(message, settingObject)
	
	if (permissionChanger.valid_change == False):
		return
	
	if (settingsType == "server"):
		await message.saveServer()
	else:
		await message.saveChannel()

async def clearPermissions(message, arguments, settingsType):
	if (settingsType == "server"):
		settingObject = message.server_settings
	else:
		settingObject = message.channel_settings
	
	language = await message.getLanguage()
	permissionChanger = PermissionChanger(arguments, language, "clear")
	await permissionChanger.parseCommands()
	
	if (permissionChanger.valid_change == False):
		return
	
	await settingObject.deletePermissions(permissionChanger.command_codes)
	
	if (settingsType == "server"):
		await message.saveServer()
	else:
		await message.saveChannel()
	
	msg = await getLanguageText(language, "PERMISSION.CLEARED")
	await send(message.discord_py.channel, msg)