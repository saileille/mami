import re
from fileIO import getCommandCode
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
	):
		self.text = text
		self.list = list
	
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
	
	async def getCommandFromString(self, language=None):
		#Get the command object based on its call name.
		#E.g. settings.server with English language would return the appropriate command object.
		#If language is not given, the text is treated as command code, not command string.
		
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
	
	async def getIdFromMention(self):
		#Returns a dictionary which tells if the mention is a user or role mention, and extracts the ID.
		#If not a role or user mention, returns None
		
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