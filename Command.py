class Command(object):
	def __init__(
		self
		,name = ""
		,short_desc = ""
		,long_desc = ""
		,sub_commands = {}
		,hidden = False
		,owner_only = False
		,all_prefixes = False
		,min_arguments = 0
		,argument_help = ""
		,argument_types = []
		,function = None
	):
		self.name = name
		self.short_desc = short_desc
		self.long_desc = long_desc
		self.sub_commands = sub_commands
		self.hidden = hidden
		self.owner_only = owner_only
		self.all_prefixes = all_prefixes
		self.min_arguments = min_arguments
		self.argument_help = argument_help
		self.argument_types = argument_types
		self.function = function
	
	async def call(self, message, callIndex, commandLevel):
		commandCall = message.calls[callIndex]
		
		if (commandCall.prefix_valid == False):
			await commandCall.validatePrefix(message, self.all_prefixes)
			
			if (commandCall.prefix_valid == False):
				return
		
		if (await self.checkOwnerOnly(message) == False):
			#TODO: function to inform the user of the inability to use this command.
			return
		
		await self.checkSubCommands(message, callIndex, commandLevel)
	
	async def checkOwnerOnly(self, message):
		from fileIO import getCsvVar
		
		if (self.owner_only == True):
			ownerId = await getCsvVar("OWNER_ID", "basic", "staticData")
			return message.discord_py.author.id == ownerId
		
		return True
	
	async def checkSubCommands(self, message, callIndex, commandLevel):
		from fileIO import getLanguageCode
		from commandFunctions import commandNotFound
		
		commandCall = message.calls[callIndex]
		incrementedCommandLevel = commandLevel + 1
		
		if (incrementedCommandLevel < len(commandCall.commands)):
			#If there are more commands in the call.
			
			commandStrIncr = commandCall.commands[incrementedCommandLevel]
			commandKey = await getLanguageCode(message.language, commandStrIncr)
			
			try:
				await self.sub_commands[commandKey].call(message, callIndex, incrementedCommandLevel)
			except KeyError:
				await commandNotFound(self, await commandCall.getCommandString())
			
			return
		
		
		if (len(self.sub_commands) > 0):
			#If the command has sub-commands but none were used...
			await self.displaySubCommands(message, await commandCall.getCommandString())
			return
		
		if (len(commandCall.arguments) < self.min_arguments):
			#If not enough arguments were given.
			await self.getSimpleHelp(message, await commandCall.getCommandString())
			return
		
		#Converting all the arguments to the proper data types. Returns True if successful.
		success = await commandCall.convertArguments(self, message)
		
		if (success == True):
			await self.function(message, commandCall.arguments)
		else:
			await self.getSimpleHelp(message, await commandCall.getCommandString())
	
	async def displaySubCommands(self, message, commandStr):
		#Used when an incomplete command gets typed.
		
		from fileIO import getLanguageText
		from bot import send
		from Prefix import Prefix
		
		prefix = await Prefix(message).getPrefix()
		
		commandStr = prefix + commandStr + "."
		subCommands = []
		
		for key in self.sub_commands:
			sub_command = self.sub_commands[key]
			
			subCmdName = await getLanguageText(message.language, sub_command.name)
			subCmdDesc = await getLanguageText(message.language, sub_command.short_desc)
			
			subCmdStr = commandStr + subCmdName + " - " + subCmdDesc
			subCommands.append(subCmdStr)
		
		msg = "```"
		
		for subCommand in subCommands:
			msg += "\n" + subCommand
		
		msg += "```"
		await send(message.discord_py.channel, msg)
	
	async def getSimpleHelp(self, message, commandStr):
		#Shows a simple syntax of the command, and displays the short description.
		#Informs the user about what is needed for the command.
		
		from fileIO import getLanguageText
		from bot import send
		from Prefix import Prefix
		
		prefix = await Prefix(message).getPrefix()
		commandStr = prefix + commandStr
		argumentStr = await getLanguageText(message.language, self.argument_help)
		shortDesc = await getLanguageText(message.language, self.short_desc)
		
		msg = "```" + commandStr + " [" + argumentStr + "]```" + shortDesc
		await send(message.discord_py.channel, msg)