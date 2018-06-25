from fileIO import getCsvVarSync
from fileIO import getDefaultPrefix, getLanguageText
from sendFunctions import processMsg

#Class for displaying the prefixes, and telling the user which one to use.
class Prefix(object):
	def __init__(self, message):
		self.user = message.user_settings.prefix
		self.channel = message.channel_settings.prefix
		
		if (message.discord_py.guild != None):
			#If in a server...
			self.server = message.server_settings.prefix
		else:
			self.server = None
		
		self.language = message.language
	
	async def getPrefixStrings(self):
		msg = await processMsg(
			"PREFIX.VIEW.DEFAULT_PREFIX"
			,self.language
			,{
				"prefix": await getDefaultPrefix()
			}
		)
		
		code = "PREFIX.VIEW.SERVER_PREFIX.NONE"
		varDict = {}
		if (self.server != None):
			code = "PREFIX.VIEW.SERVER_PREFIX"
			varDict["prefix"] = self.server
		
		msg2 = await processMsg(
			code
			,self.language
			,varDict
		)
		msg += "\n" + msg2
		
		code = "PREFIX.VIEW.CHANNEL_PREFIX.NONE"
		varDict = {}
		if (self.channel != None):
			code = "PREFIX.VIEW.CHANNEL_PREFIX"
			varDict["prefix"] = self.channel
		
		msg2 = await processMsg(
			code
			,self.language
			,varDict
		)
		msg += "\n" + msg2
		
		code = "PREFIX.VIEW.USER_PREFIX.NONE"
		varDict = {}
		if (self.user != None):
			code = "PREFIX.VIEW.USER_PREFIX"
			varDict["prefix"] = self.user
		
		msg2 = await processMsg(
			code
			,self.language
			,varDict
		)
		msg += "\n" + msg2 + "\n\n"
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
			prefix = await getDefaultPrefix()
		
		return await processMsg(
			"PREFIX.VIEW.CORRECT"
			,self.language
			,{
				"prefix": prefix
			}
		)
	
	async def getPrefix(self):
		#Can be used for building help texts - handily returns the correct prefix to use.
		
		if (self.user != None):
			return self.user
		
		if (self.server != None):
			return self.server
		
		return await getDefaultPrefix()