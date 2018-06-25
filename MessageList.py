from discord import File

from MessagePart import MessagePart

from bot import client
from fileIO import getCsvVarSync

class MessageList(object):
	block = "```"
	characterLimit = int(
		getCsvVarSync("MAX_CHARACTERS", "basic", "staticData")
	)
	
	def __init__(self, text, files):
		self.text = text
		self.files = files
		self.messages = []
	
	async def getMessageList(self):
		#Let's do this, motherfucker.
		
		#No need to go over this if the message does not need to be split.
		if (self.text == None or len(self.text) <= self.characterLimit):
			self.messages = [self.text]
			return 
		
		#List to contain all message parts.
		self.messages = [MessagePart(self.text, False, False)]
		
		#Separations.
		await self.fragmentList("```")
		await self.fragmentList("\n\n")
		await self.fragmentList("\n")
		
		#Block detection.
		await self.checkBlocks()
		
		#Catenation.
		await self.getMessages()
	
	async def fragmentList(self, separator):
		newList = []
		
		#For block counting. Paired = no active block; pairless = active block.
		counter = 0
		isBlock = False	#Checks if the current snippet of string is starting or ending a block.
		
		#Further fragments an originally existing list.
		for item in self.messages:
			i = 0
			
			while (i < len(item.message)):
				#Allows to ignore separators at the beginning of the string.
				if (i == 0):
					ignoreSeparators = True
				
				location = len(separator) + i	#Inclusive (i = exclusive).
				
				#Checking for the block.
				if (item.message[i:location] == separator and separator == self.block):
					isBlock = True
				
				if (ignoreSeparators == True and item.message[i:location] != separator):
					ignoreSeparators = False
				
				if (item.message[i:location] == separator and ignoreSeparators == False):
					if (separator == self.block):
						#Block starts.
						if (counter % 2 == 0):
							if (len(item.message[:i]) > 0):
								newList.append(MessagePart(item.message[:i], False, False))
							
							item.message = item.message[i:]
							counter -= 1	#Otherwise this block gets counted twice.
						
						#Block ends.
						else:
							if (len(item.message[:location]) > 0):
								newList.append(MessagePart(item.message[:location], False, False))
							
							item.message = item.message[location:]
					
					else:
						if (len(item.message[:i]) > 0):
							newList.append(MessagePart(item.message[:i], False, False))
						item.message = item.message[i:]
					
					i = 0
				
				else:
					i += 1
				
				#Everything block-related.
				if (isBlock):
					isBlock = False
					counter += 1
					
					if (i > 0):
						i += (len(self.block) - 1)
			
			newList.append(item)
		
		self.messages = newList
	
	async def checkBlocks(self):
		#Detects where blocks go.
		counter = 0
		
		for item in self.messages:
			if (counter % 2 != 0):
				item.start_block = True
			
			i = 0
			while (i < len(item.message)):
				location = len(self.block) + i
				if (item.message[i:location] == self.block):
					counter += 1
					i += len(self.block) - 1
				
				i += 1
			
			if (counter % 2 != 0):
				item.end_block = True
	
	async def getMessages(self):
		messages = []
		msg = ""
		
		i = 0
		while (i < len(self.messages)):
			if (len(msg) == 0):
				if (self.messages[i].start_block):
					msg += self.block
				
				msg += self.messages[i].message
			
			else:
				#itemLength = len(self.messages[i].message)
				end = ""
				if (self.messages[i].end_block):
					end = self.block
				
				if (len((msg + self.messages[i].message + end).strip()) > self.characterLimit):
					if (self.messages[i-1].end_block):
						msg += self.block
					
					messages.append(msg.strip())
					msg = ""
					i -= 1
				
				else:
					msg += self.messages[i].message
			
			i += 1
		
		messages.append(msg.strip())
		self.messages = messages
	
	async def sendMessages(self, channel):
		sentMessages = []
		
		for i in range(len(self.messages)):
			if (i == 0 and self.files != None):
				await self.convertToFileObjects()
				
				if (len(self.files) == 1):
					sentMessages.append(
						await channel.send(
							content = self.messages[i]
							,file = self.files[i]
						)
					)
				else:
					sentMessages.append(
						await channel.send(
							content = self.messages[i]
							,files = self.files
						)
					)
			else:
				sentMessages.append(
					await channel.send(self.messages[i])
				)
		
		return sentMessages
	
	#Converts the file paths to objects of File class.
	async def convertToFileObjects(self):
		fileObjects = []
		for filePath in self.files:
			fileObjects.append(
				File(filePath)
			)
		
		self.files = fileObjects