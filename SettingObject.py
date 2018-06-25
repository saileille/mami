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
			await send(
				message.discord_py.channel
				,"PREFIX.{TYPE}.CHANGE.NO_DIFFERENCE".format(TYPE=className)
				,message.language
				,{
					"prefix": self.prefix
				}
			)
			return
		
		self.prefix = newPrefix
		
		await message.save()
		
		await send(
			message.discord_py.channel
			,"PREFIX.{TYPE}.CHANGE.COMPLETED".format(TYPE=className)
			,message.language
			,{
				"user": message.discord_py.author.display_name
				,"prefix": self.prefix
			}
		)
	
	async def clearPrefix(self, message):
		className = type(self).__name__.upper()
		self.prefix = None
		await message.save()
		
		await send(
			message.discord_py.channel
			,"PREFIX.{TYPE}.CLEAR.CLEARED".format(TYPE=className)
			,message.language
		)
	
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
		
		await send(
			message.discord_py.channel
			,"PERMISSIONS_CLEARED"
			,message.language
		)
	
	async def changeLanguage(self, message, arguments):
		className = type(self).__name__.upper()
		languageName = " ".join(arguments)
		languageCode = await getLanguageCode(message.language, languageName)
		
		msg = "INVALID_LANGUAGE_NAME"
		varDict = {}
		
		if (languageCode != None):
			self.language = languageCode
			
			await message.save()
			await message.getLanguage()
			
			msg = "SETTINGS.{TYPE}.LANGUAGE.CHANGE.CHANGED".format(TYPE=className)
		else:
			varDict["language"] = languageName
			varDict["languages"] = "\n".join(
				await getExistingLanguages(message.language)
			)
		
		await send(
			message.discord_py.channel
			,msg
			,message.language
			,varDict
		)
	
	async def clearLanguage(self, message):
		className = type(self).__name__.upper()
		
		self.language = None
		await message.save()
		await message.getLanguage()
		
		await send(
			message.discord_py.channel
			,"SETTINGS.{TYPE}.LANGUAGE.CLEAR.RESET".format(TYPE=className)
			,message.language
		)
	
	#Returns True if valid prefix, False if not, and None if undetermined.
	async def checkPrefix(self, usedPrefix):
		if (self.prefix == None):
			return None
		
		if (self.prefix == usedPrefix):
			return True
		
		return False