from bot import send
from fileIO import getCsvVarSync
from fileIO import getLanguageText
from fileIO import savePickle
from Prefix import Prefix

class User(object):
	defaultLanguage = getCsvVarSync("DEFAULT_LANGUAGE", "basic", "staticData")
	
	def __init__(
		self
		,prefix = None
		,rpg_character = None
		,language = defaultLanguage
	):
		self.prefix = prefix
		self.rpg_character = rpg_character
		self.language = language
	
	async def isDefault(self):
		#Checks if the User object is the default one.
		if (self.prefix != None):
			return False
		
		if (self.rpg_character != None):
			return False
		
		if (self.language != self.defaultLanguage):
			return False
		
		return True
	
	async def changePrefix(self, message, newPrefix):
		#For display purposes.
		newPrefixStr = newPrefix
		
		if (newPrefix == Prefix(message).default):
			newPrefix = None
		
		if (newPrefix == self.prefix):
			msg = await getLanguageText(await message.getLanguage(), "COMMAND.PREFIX.USER.NO_DIFFERENCE")
			msg = msg.format(prefix=self.prefix)
			
			await send(message.discord_py.channel, msg)
			return
		
		self.prefix = newPrefix
		
		msg = await getLanguageText(await message.getLanguage(), "COMMAND.PREFIX.USER.CHANGED")
		msg = msg.format(user=message.discord_py.author.display_name, prefix=newPrefixStr)
		
		await send(message.discord_py.channel, msg)
	
	async def save(self, message):
		folder = "savedData\\users"
		await savePickle(self, message.author.id, folder)