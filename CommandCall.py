from Prefix import Prefix
from StringHandler import StringHandler

from fileIO import getCommandCodeList, getDefaultPrefix, getLanguageText
from sendFunctions import processMsg

class CommandCall(object):
	def __init__(self, raw_text=""):
		self.raw_text = raw_text
		self.prefix = None
		self.command_strings = None
		self.commands = []
		self.arguments = []
	
	async def process(self, customPrefixes, language):
		prefixes = [await getDefaultPrefix()]
		for prefix in customPrefixes:
			if (prefix != None):
				prefixes.append(prefix)
		
		#Sorts the command calls appropriately.
		for prefix in prefixes:
			if (self.raw_text.startswith(prefix)):
				await self.getPrefix(prefix)
				break
		else:
			#No prefix, no fun.
			self.arguments = None
			self.commands = None
			return
		
		await self.getCommandsAndArguments(language)
	
	async def getPrefix(self, prefix):
		self.raw_text = self.raw_text[len(prefix):]
		self.prefix = prefix
	
	async def getCommandsAndArguments(self, language):
		#Gives command list and argument list.
		parts = self.raw_text.split(" ")
		self.arguments = parts[1:]
		self.command_strings = parts[0].split(".")
		
		self.commands = await getCommandCodeList(language, self.command_strings)
	
	#called: True if the command is to be called.
	async def validatePrefix(self, message, allPrefixesAllowed, called):
		if (allPrefixesAllowed == True and called == True):
			return True
		
		#User prefix check.
		prefixCheck = await message.user_settings.checkPrefix(self.prefix)
		if (prefixCheck != None):
			return prefixCheck
		
		#Channel and guild prefix checks.
		if (message.discord_py.guild != None):
			prefixCheck = await message.channel_settings.checkPrefix(self.prefix)
			if (prefixCheck != None):
				return prefixCheck
			
			prefixCheck = await message.server_settings.checkPrefix(self.prefix)
			if (prefixCheck != None):
				return prefixCheck
		
		#Default prefix check.
		if (await getDefaultPrefix() == self.prefix):
			return True
		
		return False
	
	#Converts the arguments of the call according to the specification in Command object.
	async def convertArguments(self, command, language):
		newArguments = []
		for i in range(len(self.arguments)):
			argument = self.arguments[i]
			
			try:
				argumentRule = command.argument_types[i]
			except IndexError:
				#If there are more than the minimum amount of arguments.
				argumentRule = command.optional_arguments_type
			
			#Regex check.
			if (await argumentRule.checkArgument(argument) == False):
				msg = await processMsg(
					argumentRule.fail_description
					,language
				)
				return msg
			
			#Argument conversion.
			convertedArgument = await argumentRule.convertArgument(argument)
			
			if (convertedArgument == None):
				return await processMsg(
					"ARGUMENT_CONV_ERROR"
					,language
					,{
						"argument": argument
					}
				)
			
			#Range check.
			if (await argumentRule.checkRange(convertedArgument) == False):
				return await processMsg(
					"ARGUMENT_NOT_IN_RANGE"
					,language
					,{
						"range": argumentRule.num_range
					}
				)
			
			newArguments.append(convertedArgument)
		
		self.arguments = newArguments
		return ""
	
	async def trimCommandStrings(self, index):
		#index is the index of last acceptable command.
		if (index != -1):
			self.command_strings = self.command_strings[:index + 1]
		else:
			self.command_strings = []
	
	#Gives command string of a specified length (determined by commandIndex).
	async def getTrimmedCommandString(self, message, commandIndex):
		prefix = await Prefix(message).getPrefix()
		await self.trimCommandStrings(commandIndex)
		commandStr = ".".join(self.command_strings)
		commandStr = prefix + commandStr
		
		return commandStr