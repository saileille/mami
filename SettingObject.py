from PermissionChanger import PermissionChanger

from fileIO import getExistingLanguages
from fileIO import getLanguageCode
from fileIO import getLanguageText
from sendFunctions import send

#All sorts of functions shared between server, channel and user settings
class SettingObject(object):
	def __init__(
		self
		,language = None
		,prefix = None
	):
		self.language = language
		self.prefix = prefix
	
	async def changePrefix(self, message, arguments):
		className = type(self).__name__.upper()
		newPrefix = " ".join(arguments)
		
		if (newPrefix == self.prefix):
			msg = await getLanguageText(
				message.language
				,"PREFIX.{TYPE}.CHANGE.NO_DIFFERENCE".format(TYPE=className)
			)
			msg = msg.format(prefix=self.prefix)
			
			await send(message.discord_py.channel, msg)
			return
		
		self.prefix = newPrefix
		
		msg = await getLanguageText(
			message.language
			,"PREFIX.{TYPE}.CHANGE.COMPLETED".format(TYPE=className)
		)
		msg = msg.format(user=message.discord_py.author.display_name, prefix=self.prefix)
		
		await message.save()
		await send(message.discord_py.channel, msg)
	
	async def clearPrefix(self, message):
		className = type(self).__name__.upper()
		self.prefix = None
		await message.save()
		
		msg = await getLanguageText(
			message.language
			,"PREFIX.{TYPE}.CLEAR.CLEARED".format(TYPE=className)
		)
		await send(message.discord_py.channel, msg)
	
	async def changePermissions(self, message, arguments, operation):
		permissionChanger = PermissionChanger(arguments, message.language, operation)
		await permissionChanger.changePermissions(message, self)
		
		if (permissionChanger.valid_change == False):
			return
		
		await message.save()
	
	#Clears all given permissions for specific command(s)
	async def clearPermissions(self, message, arguments):
		permissionChanger = PermissionChanger(arguments, message.language, "clear")
		await permissionChanger.parseCommands(message)
		
		if (permissionChanger.valid_change == False):
			return
		
		await self.deletePermissions(permissionChanger.command_codes)
		await message.save()
		
		msg = await getLanguageText(message.language, "PERMISSIONS_CLEARED")
		await send(message.discord_py.channel, msg)
	
	async def changeLanguage(self, message, arguments):
		className = type(self).__name__.upper()
		languageName = " ".join(arguments)
		languageCode = await getLanguageCode(message.language, languageName)
		
		if (languageCode != None):
			self.language = languageCode
			await message.save()
			await message.getLanguage()
			
			await send(
				message.discord_py.channel
				,await getLanguageText(
					message.language
					,"SETTINGS.{TYPE}.LANGUAGE.CHANGE.CHANGED".format(TYPE=className)
				)
			)
		else:
			msg = await getLanguageText(message.language, "INVALID_LANGUAGE_NAME")
			msg = msg.format(
				language = languageName
				,languages = "\n".join(await getExistingLanguages(message.language))
			)
			
			await send(message.discord_py.channel, msg)
	
	async def clearLanguage(self, message):
		className = type(self).__name__.upper()
		
		self.language = None
		await message.save()
		await message.getLanguage()
		
		await send(
			message.discord_py.channel
			,await getLanguageText(
				message.language
				,"SETTINGS.{TYPE}.LANGUAGE.CLEAR.RESET".format(TYPE=className)
			)
		)
	
	#Returns True if valid prefix, False if not, and None if undetermined.
	async def checkPrefix(self, usedPrefix):
		if (self.prefix == None):
			return None
		
		if (self.prefix == usedPrefix):
			return True
		
		return False