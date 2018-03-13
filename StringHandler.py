#Has all sorts of string-conversion functions.

class StringHandler(object):
	#Regex patterns
	userMention = "<@!?([0-9]{18})>"
	roleMention = "<@&([0-9]{18})>"
	
	def __init__(self, text):
		self.text = text
	
	async def getCommandCodeList(self, language):
		#Converts the command string to a list of command codes.
		
		from fileIO import getCommandCode
		
		commandList = self.text.split(".")
		
		codeList = []
		for text in commandList:
			commandCode = await getCommandCode(language, text, codeList)
			codeList.append(commandCode)
			
			if (commandCode == None):
				break
		
		return codeList
	
	async def getIdFromMention(self):
		#Returns a dictionary which tells if the mention is a user or role mention, and extracts the ID.
		#If not a role or user mention, returns None
		import re
		
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