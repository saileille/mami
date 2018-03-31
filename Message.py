from Channel import Channel
from CommandCall import CommandCall
from commandFunctions import commandNotFound
from fileIO import deleteFile
from fileIO import getDefaultLanguage
from fileIO import loadCommands
from fileIO import loadPickle
from fileIO import savePickle
from Server import Server
from User import User

class Message(object):
	def __init__(
		self
		,discord_py
	):
		#The Message object from Discord.py
		self.discord_py = discord_py
		
		#Own stuff.
		self.calls = []
		self.user_settings = None
		self.server_settings = None
		self.channel_settings = None
	
	async def separate(self):
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
		commands = await loadCommands()
		
		#Going through every command call.
		for i in range(len(self.calls)):
			#commandCall = self.calls[i]
			#commandKey = commandCall.commands[0]
			
			await commands.call(self, i, -1)
	
	async def getUserSettings(self):
		try:
			self.user_settings = await loadPickle(self.discord_py.author.id, "savedData\\users")
		except FileNotFoundError:
			user = User()
			await user.forceDefault()
			self.user_settings = user
	
	async def getServerSettings(self):
		try:
			self.server_settings = await loadPickle(self.discord_py.server.id, "savedData\\servers")
		except FileNotFoundError:
			server = Server()
			await server.forceDefault()
			self.server_settings = server
	
	async def getChannelSettings(self):
		try:
			self.channel_settings = await loadPickle(self.discord_py.channel.id, "savedData\\channels")
		except FileNotFoundError:
			channel = Channel()
			await channel.forceDefault()
			self.channel_settings = channel
	
	async def getSettings(self):
		#Loads user and server settings.
		await self.getUserSettings()
		await self.getChannelSettings()
		
		if (self.discord_py.server != None):
			await self.getServerSettings()
	
	async def getLanguage(self):
		if (self.channel_settings.language != None):
			return self.channel_settings.language
		
		if (self.discord_py.server != None):
			#If in server...
			if (self.server_settings.language != None):
				return self.server_settings.language
			
			return await getDefaultLanguage
		
		if (self.user_settings.language != None):
			return self.user_settings.language
		
		return await getDefaultLanguage
	
	async def saveServer(self):
		folder = "savedData\\servers"
		filename = self.discord_py.server.id
		
		if (await self.server_settings.isDefault() == False):
			await savePickle(self.server_settings, filename, folder)
		else:
			await deleteFile(filename + ".db", folder)
	
	async def saveUser(self):
		folder = "savedData\\users"
		filename = self.discord_py.author.id
		
		if (await self.user_settings.isDefault() == False):
			await savePickle(self.user_settings, filename, folder)
		else:
			await deleteFile(filename + ".db", folder)
	
	async def saveChannel(self):
		folder = "savedData\\channels"
		filename = self.discord_py.channel.id
		
		if (await self.channel_settings.isDefault() == False):
			await savePickle(self.channel_settings, filename, folder)
		else:
			await deleteFile(filename + ".db", folder)