import re
from bot import client
from fileIO import getCommandCode
from fileIO import getCommandName
from fileIO import getLanguageText
from fileIO import loadCommands

#Has all sorts of string-conversion functions, both to and from string.

class StringHandler(object):
	#Regex patterns
	userMention = "<@!?([0-9]{18})>"
	roleMention = "<@&([0-9]{18})>"
	
	def __init__(
		self
		,text = None
		,list = None
		,dict = None
	):
		self.text = text
		self.list = list
		self.dict = dict
	
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
	async def getLocalisedCommandString(self, language, commandCode):
		codeList = commandCode.split(".")
		nameList = []
		for i in range(len(codeList)):
			nameList.append(
				await getCommandName(language, codeList[i], codeList[:i])
			)
		
		commandName = ".".join(nameList)
		return commandName
	
	#Returns a dictionary which tells if the mention is a user or role mention, and extracts the ID.
	#If not a role or user mention, returns None
	async def getIdFromMention(self):
		isUser = re.fullmatch(self.userMention, self.text)
		if (isUser != None):
			id = isUser.group(1)
			
			dictionary = {
				"type": "user"
				,"id": id
			}
			
			return dictionary
		
		isRole = re.fullmatch(self.roleMention, self.text)
		if (isRole != None):
			id = isRole.group(1)
			
			dictionary = {
				"type": "role"
				,"id": id
			}
			
			return dictionary
		
		return isRole
	
	async def getChapterDivide(self):
		string = ""
		for item in self.list:
			if (string != ""):
				string += "\n\n"
			
			string += item
		
		return string
	
	#Returns a nice text thing. (Well said!)
	async def getPermissionInfoText(self, discordMessage, language):
		msgList = []
		
		for key in self.dict:
			msgList.append(
				await self.getLocalisedCommandString(language, key)
			)
			
			if ("server" in self.dict[key]):
				permissionObject = self.dict[key]["server"]
				
				msgList.append(
					await getLanguageText(language, "SERVER")
				)
				
				msgList += await permissionObject.getPermissionString(discordMessage, language)
			
			if ("channels" in self.dict[key]):
				msgList.append(
					await getLanguageText(language, "OVERRIDDEN_CHANNELS")
				)
				
				for channelKey in self.dict[key]["channels"]:
					#Get the channel object.
					channelObject = client.get_channel(channelKey)
					msgList.append(channelObject.name)
					
					permissionObject = self.dict[key]["channels"][channelKey]
					msgList += await permissionObject.getPermissionString(discordMessage, language)
		
		if (len(msgList) == 0):
			msgList.append(
				await getLanguageText(language, "INFO.PERMISSIONS.NO_PERMISSIONS_ON_SERVER")
			)
		
		self.list = msgList
		return await self.getChapterDivide()