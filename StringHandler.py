import re
from fileIO import getCommandCode
from fileIO import getCommandName
from fileIO import loadCommands

#Has all sorts of string-conversion functions.
class StringHandler(object):
	#Regex patterns
	#Mentioning works, as well as writing a letter indicating the type, and ID.
	regexPatterns = {
		"user": "<@!?([0-9]{18})>|u([0-9]{18})"
		,"role": "<@&([0-9]{18})>|r([0-9]{18})"
		,"channel": "<#([0-9]{18})>|c([0-9]{18})"
	}
	
	def __init__(
		self
		,text = None
	):
		self.text = text
	
	async def getCommandCodeList(self, language):
		#Converts the command string to a list of command codes.
		commandList = self.text.split(".")
		
		codeList = []
		for text in commandList:
			commandCode = await getCommandCode(language, text, codeList)
			codeList.append(commandCode)
			
			if (commandCode == None):
				break
		
		return codeList
	
	#Get the command object based on its call name.
	#E.g. settings.server with English language would return the appropriate command object.
	#If language is not given, the text is treated as command code, not command string.
	async def getCommandFromString(self, language=None):
		if (language == None):
			codeList = self.text.split(".")
		else:
			codeList = await self.getCommandCodeList(language)
		
		if (codeList[-1] == None):
			return None
		
		commandObject = await loadCommands()
		
		for code in codeList:
			commandObject = commandObject.sub_commands[code]
		
		return commandObject
	
	#Takes the absolute command code, returns localised command name.
	#Used for e.g. getting command permissions to show to the user.
	async def getLocalisedCommandString(self, language):
		codeList = self.text.split(".")
		nameList = []
		for i in range(len(codeList)):
			nameList.append(
				await getCommandName(language, codeList[i], codeList[:i])
			)
		
		commandName = ".".join(nameList)
		return commandName
	
	async def getId(self, type):
		idMatch = re.fullmatch(self.regexPatterns[type], self.text)
		
		if (idMatch != None):
			for i in range(1, 3):
				id = idMatch.group(i)
				if (id != None):
					return int(id)
		
		return None
	
	#Returns a dictionary which tells if the mention is a user or role mention, and extracts the ID.
	#If not a role or user mention, returns None
	async def getUserOrChannelId(self):
		userId = await self.getId("user")
		
		if (userId != None):
			dictionary = {
				"type": "user"
				,"id": userId
			}
			
			return dictionary
		
		roleId = await self.getId("role")
		if (roleId != None):
			dictionary = {
				"type": "role"
				,"id": roleId
			}
			
			return dictionary
		
		return None
	
	#Gives either server, channel or user settings as a settingObject.
	async def getSettingObject(self, message):
		if (self.text == "server"):
			return message.server_settings
		
		if (self.text == "channel"):
			return message.channel_settings
		
		return message.user_settings