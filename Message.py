class Message(object):
	def __init__(
		self
		,discord_py
	):
		#The Message object from Discord.py
		self.discord_py = discord_py
		self.calls = []
		self.user_settings = None
		self.server_settings = None
	
	async def separate(self):
		from CommandCall import CommandCall
		
		#Separates the message according to its lines.
		lines = self.discord_py.content.split("\n")
		
		commandCalls = []
		#Processes commands and organises them.
		for line in lines:
			call = CommandCall(line)
			
			prefixList = [self.user_settings.prefix]
			
			if (self.discord_py.server != None):
				prefixList.append(self.server_settings.prefix)
			
			await call.process(prefixList, await self.getLanguage())
			
			if (call.arguments != None and call.commands != None):
				commandCalls.append(call)
		
		self.calls = commandCalls
	
	async def executeCommands(self):
		from fileIO import loadPickle
		from commandFunctions import commandNotFound
		
		commands = await loadPickle("commandDict", folder="staticData")
		
		#Going through every command call.
		for i in range(len(self.calls)):
			#commandCall = self.calls[i]
			#commandKey = commandCall.commands[0]
			
			await commands.call(self, i, -1)
			
			"""
			try:
				#This function contains all necessary checks etc.
				await commands[commandKey].call(self, i, 0)
			except KeyError:
				await commandNotFound(self, await commandCall.getCommandString())
			"""
	
	async def getUserSettings(self):
		from fileIO import loadPickle
		from User import User
		
		self.user_settings = await loadPickle(
			self.discord_py.author.id
			,"savedData\\users"
			,User()
		)
	
	async def getServerSettings(self):
		from fileIO import loadPickle
		from Server import Server
		
		self.server_settings = await loadPickle(
			self.discord_py.server.id
			,"savedData\\servers"
			,Server()
		)
	
	async def getSettings(self):
		#Loads user and server settings.
		await self.getUserSettings()
		
		if (self.discord_py.server != None):
			await self.getServerSettings()
	
	async def getLanguage(self):
		if (self.discord_py.server != None):
			return self.server_settings.language
		else:
			return self.user_settings.language