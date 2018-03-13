class CommandCall(object):
	from fileIO import getCsvVarSync
	
	defaultPrefix = getCsvVarSync("DEFAULT_PREFIX", "basic", "staticData")
	
	def __init__(
		self
		,raw_text = ""
	):
		self.raw_text = raw_text
		self.prefix = None
		self.command_strings = None
		
		#Validation happens at the first command check.
		self.prefix_valid = False
		
		self.commands = []
		self.arguments = []
	
	async def process(self, customPrefixes, language):
		prefixes = [self.defaultPrefix]
		
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
		
		await self.convertCommands(language)
	
	async def validatePrefix(self, message, allPrefixesAllowed):
		if (allPrefixesAllowed == True):
			self.prefix_valid = True
			return
		
		#User prefix check.
		if (message.user_settings.prefix != None):
			#Not sure why we need to check for None. Come back to this later.
			if (message.user_settings.prefix == self.prefix):
				self.prefix_valid = True
			
			return
		
		#Server prefix check.
		if (message.discord_py.server != None):
			#Causes exception if the server is not checked for None value.
			#Alternative would be to make a ghost server object.
			if (message.server_settings.prefix != None):
				if (message.server_settings.prefix == self.prefix):
					self.prefix_valid = True
				
				return
		
		#Default prefix check.
		if (self.defaultPrefix == self.prefix):
			self.prefix_valid = True
	
	async def convertArguments(self, command, language):
		#Converts the arguments of the call according to the specification in Command object.
		
		from fileIO import getLanguageText
		
		newArguments = []
		for i in range(len(self.arguments)):
			argument = self.arguments[i]
			
			try:
				type = command.argument_types[i]
			except IndexError:
				#If there are more than the minimum amount of arguments, the last conversion rule will be used.
				type = command.argument_types[-1]
			
			try:
				if (type == "int"):
					argument = int(argument)
				elif (type == "float"):
					argument = float(argument)
			
			except ValueError:
				msg = await getLanguageText(language, "COMMAND.ARGUMENT_CONV.ERROR")
				msg = msg.format(argument=argument)
				
				return msg
			
			newArguments.append(argument)
		
		self.arguments = newArguments
		return ""
	
	async def convertCommands(self, language):
		#Converts the command string to a list of command codes.
		
		from fileIO import getCommandCode
		from StringHandler import StringHandler
		
		commandText = await self.getCommandString()
		self.commands = await StringHandler(commandText).getCommandCodeList(language)
	
	async def getCommandString(self):
		commandString = ".".join(self.command_strings)
		
		return commandString
	
	async def trimCommandStrings(self, index):
		#index is the index of last acceptable command.
		if (index != -1):
			self.command_strings = self.command_strings[:index + 1]
		else:
			self.command_strings = []
	
	async def getTrimmedCommandString(self, message, commandIndex):
		#Gives command string of a specified length (determined by commandIndex).
		from Prefix import Prefix
		
		prefix = await Prefix(message).getPrefix()
		await self.trimCommandStrings(commandIndex)
		commandStr = await self.getCommandString()
		commandStr = prefix + commandStr
		
		return commandStr