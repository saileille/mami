class CommandCall(object):
	from fileIO import getCsvVarSync
	
	defaultPrefix = getCsvVarSync("DEFAULT_PREFIX", "basic", "staticData")
	
	def __init__(
		self
		,raw_text = ""
	):
		self.raw_text = raw_text
		self.prefix = None
		
		#Validation happens at the first command check.
		self.prefix_valid = False
		
		self.commands = []
		self.arguments = []
	
	async def process(self, customPrefixes):
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
		
		await self.getCommandsAndArguments()
	
	async def getPrefix(self, prefix):
		self.raw_text = self.raw_text[len(prefix):]
		self.prefix = prefix
	
	async def getCommandsAndArguments(self):
		#Gives command list and argument list.
		parts = self.raw_text.split(" ")
		self.arguments = parts[1:]
		
		commandParts = parts[0].split(".")
		self.commands = commandParts
	
	async def getCommandString(self):
		commandStr = ""
		
		for i in range(len(self.commands)):
			if (i > 0):
				commandStr += "."
			commandStr += self.commands[i]
		
		return commandStr
	
	async def validatePrefix(self, message, allPrefixesAllowed):
		if (allPrefixesAllowed == True):
			self.prefix_valid = True
			return
		
		if (message.user_settings.prefix != None):
			if (message.user_settings.prefix == self.prefix):
				self.prefix_valid = True
			
			return
		
		if (message.discord_py.server != None):
			#Causes exception if the server is not checked for None value.
			#Alternative would be to make a ghost server object.
			if (message.server_settings.prefix != None):
				if (message.server_settings.prefix == self.prefix):
					self.prefix_valid = True
				
				return
		
		if (self.defaultPrefix == self.prefix):
			self.prefix_valid = True
	
	async def convertArguments(self, command, message):
		#Converts the arguments of the call according to the specification in Command object.
		
		from fileIO import getLanguageText
		from bot import send
		
		newArguments = []
		
		for i in range(len(command.argument_types)):
			argument = self.arguments[i]
			type = command.argument_types[i]
			
			try:
				if (type == "int"):
					argument = int(argument)
				elif (type == "float"):
					argument = float(argument)
			
			except ValueError:
				msg = await getLanguageText(message.language, "COMMAND.ARGUMENT_CONV.ERROR")
				msg = msg.format(argument=argument)
				await send(message.discord_py.channel, msg)
				
				return False
			
			newArguments.append(argument)
		
		self.arguments = newArguments
		return True