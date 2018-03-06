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
			await call.process(self.user_settings.prefix)
			
			if (call.arguments != None and call.commands != None):
				commandCalls.append(call)
		
		self.calls = commandCalls
	
	async def executeCommands(self):
		from commandFunctions import commandHandler
		from fileIO import loadPickle
		from fileIO import getLanguageVar
		from commandFunctions import commandNotFound
		
		commands = await loadPickle("commandDict", folder="staticData")
		
		#Going through every command call.
		for i in range(len(self.calls)):
			commandCall = self.calls[i]
			commandStr = commandCall.commands[0]
			
			commandKey = await getLanguageVar(self.server_settings.language, commandStr)
			
			try:
				#This function contains all necessary checks etc.
				await commands[commandKey].call(self, i)
			except KeyError:
				await commandNotFound(self, commandStr)
	
	async def getUserSettings(self):
		from fileIO import loadPickle
		from fileIO import getCsvVar
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












		