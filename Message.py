from Channel import Channel
from CommandCall import CommandCall
from Server import Server
from User import User

from fileIO import getDefaultLanguage, loadCommands, loadPickle
from settingObjectIO import loadChannelSettings, loadServerSettings, loadUserSettings, saveSettingObject

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
		self.language = None
	
	async def separate(self):
		prefixList = [self.user_settings.prefix]
		if (self.discord_py.guild != None):
			prefixList.append(self.server_settings.prefix)
			prefixList.append(self.channel_settings.prefix)
		
		#Separates the message according to its lines.
		lines = self.discord_py.content.split("\n")
		
		#Processes commands and organises them.
		for line in lines:
			call = CommandCall(line)
			await call.process(prefixList, self.language)
			
			if (call.arguments != None and call.commands != None):
				self.calls.append(call)
	
	async def executeCommands(self):
		commands = await loadCommands()
		
		#Going through every command call.
		for i in range(len(self.calls)):
			await commands.call(self, i, -1)
	
	#Loads user, channel and server settings, and sets up the language.
	async def getSettings(self):
		self.user_settings = await loadUserSettings(self.discord_py.author.id)
		self.channel_settings = await loadChannelSettings(self.discord_py.channel.id)
		
		if (self.discord_py.guild != None):
			self.server_settings = await loadServerSettings(self.discord_py.guild.id)
		
		await self.getLanguage()
	
	#Assigning the language as an attribute to limit processing and to avoid hassle with async and sync.
	async def getLanguage(self):
		#If channel language has been defined, that is used.
		if (self.channel_settings.language != None):
			self.language = self.channel_settings.language
			return
		
		if (self.discord_py.guild != None):
			if (self.server_settings.language != None):
				self.language = self.server_settings.language
				return
			
			#If in server, user's language is not even considered.
			self.language = await getDefaultLanguage()
			return
		
		#If in private channel...
		if (self.user_settings.language != None):
			self.language = self.user_settings.language
			return
		
		self.language = await getDefaultLanguage()
	
	#Saves server, user and channel in one function.
	async def save(self):
		if (self.server_settings != None):
			await saveSettingObject(self.server_settings, self.discord_py.guild.id)
			await saveSettingObject(self.channel_settings, self.discord_py.channel.id)
		
		await saveSettingObject(self.user_settings, self.discord_py.author.id)