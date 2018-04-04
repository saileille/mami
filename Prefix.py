from fileIO import getCsvVarSync
from fileIO import getLanguageText

#Class for displaying the prefixes, and telling the user which one to use.
class Prefix(object):
	default = getCsvVarSync("DEFAULT_PREFIX", "basic", "staticData")
	
	def __init__(self, message):
		self.user = message.user_settings.prefix
		self.channel = message.channel_settings.prefix
		
		if (message.discord_py.server != None):
			#If in a server...
			self.server = message.server_settings.prefix
		else:
			self.server = None
		
		self.language = message.language
	
	async def getPrefixStrings(self):
		msg = await getLanguageText(self.language, "PREFIX.VIEW.DEFAULT_PREFIX")
		msg = msg.format(prefix=self.default)
		
		string = ""
		if (self.server != None):
			string = await getLanguageText(self.language, "PREFIX.VIEW.SERVER_PREFIX")
			string = string.format(prefix=self.server)
		else:
			string = await getLanguageText(self.language, "PREFIX.VIEW.SERVER_PREFIX.NONE")
		
		msg += "\n" + string
		
		if (self.channel != None):
			string = await getLanguageText(self.language, "PREFIX.VIEW.CHANNEL_PREFIX")
			string = string.format(prefix=self.channel)
		else:
			string = await getLanguageText(self.language, "PREFIX.VIEW.CHANNEL_PREFIX.NONE")
		
		msg += "\n" + string
		
		if (self.user != None):
			string = await getLanguageText(self.language, "PREFIX.VIEW.USER_PREFIX")
			string = string.format(prefix=self.user)
		else:
			string = await getLanguageText(self.language, "PREFIX.VIEW.USER_PREFIX.NONE")
		
		msg += "\n" + string + "\n\n"
		msg += await self.getPrefixText()
		
		return msg
	
	async def getPrefixText(self):
		#Used for prefix.view - tells the user which prefix to use.
		if (self.user != None):
			prefix = self.user
		elif (self.channel != None):
			prefix = self.channel
		elif (self.server != None):
			prefix = self.server
		else:
			prefix = self.default
		
		text = await getLanguageText(self.language, "PREFIX.VIEW.CORRECT")
		text = text.format(prefix=prefix)
		return text
	
	async def getPrefix(self):
		#Can be used for building help texts - handily returns the correct prefix to use.
		
		if (self.user != None):
			return self.user
		
		if (self.server != None):
			return self.server
		
		return self.default