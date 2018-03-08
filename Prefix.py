#Class for displaying the prefixes, and telling the user which one to use.

class Prefix(object):
	from fileIO import getCsvVarSync
	
	default = getCsvVarSync("DEFAULT_PREFIX", "basic", "staticData")
	
	def __init__(self, message):
		if (message.discord_py.server != None):
			self.server = message.server_settings.prefix
		else:
			self.server = None
		
		self.user = message.user_settings.prefix
		self.language = message.language
	
	async def getPrefixStrings(self):
		from fileIO import getLanguageText
		
		msg = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.DEFAULT_PREFIX")
		msg = msg.format(prefix=self.default)
		
		string = ""
		if (self.server != None):
			string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.SERVER_PREFIX")
			string = string.format(prefix=self.server)
		else:
			string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.SERVER_PREFIX.NONE")
		
		msg += "\n" + string
		
		if (self.user != None):
			string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.USER_PREFIX")
			string = string.format(prefix=self.user)
		else:
			string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.USER_PREFIX.NONE")
		
		msg += "\n" + string + "\n\n"
		
		msg += await self.getPrefixText()
		
		return msg
	
	async def getPrefixText(self):
		#Used for prefix.view - tells the user which prefix to use.
		
		from fileIO import getLanguageText
		
		if (self.user != None):
			string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.CORRECT.USER")
			string = string.format(prefix=self.user)
			return string
		
		if (self.server != None):
			string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.CORRECT.SERVER")
			string = string.format(prefix=self.server)
			return string
		
		string = await getLanguageText(self.language, "COMMAND.PREFIX.VIEW.CORRECT.DEFAULT")
		string = string.format(prefix=self.default)
		return string
	
	async def getPrefix(self):
		#Can be used for building help texts - handily returns the correct prefix to use.
		
		if (self.user != None):
			return self.user
		
		if (self.server != None):
			return self.server
		
		return self.default