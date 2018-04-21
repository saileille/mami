from Prefix import Prefix

from permissionFunctions import checkCommandPermission
from fileIO import getCommandName
from fileIO import getCsvVar
from fileIO import getExistingLanguages
from fileIO import getLanguageCode
from fileIO import getLanguageText
from fileIO import readTextFile
from sendFunctions import send

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
		,argument_help = ""
		,argument_types = []
		,optional_arguments_type = None
		,default_permissions = []
		,function = None
		,nsfw_function = None
	):
		self.name = name
		self.short_desc = short_desc
		self.long_desc = long_desc
		self.sub_commands = sub_commands
		self.hidden = hidden
		self.owner_only = owner_only
		self.all_prefixes = all_prefixes
		self.argument_help = argument_help
		self.argument_types = argument_types
		self.optional_arguments_type = optional_arguments_type
		self.default_permissions = default_permissions
		self.function = function
		self.nsfw_function = nsfw_function
	
	async def call(self, message, callIndex, commandIndex):
		commandCall = message.calls[callIndex]
		
		#Validating the prefix. Execution will not continue if invalid.
		if (await commandCall.validatePrefix(message, self.all_prefixes) == False):
			return
		
		#TODO: function to inform the user of the inability to use this command.
		if (await self.checkOwnerOnly(message) == False):
			return
		
		if (
			commandIndex != -1
			and await checkCommandPermission(
				message.discord_py.author
				,message.server_settings
				,message.channel_settings
				,commandCall.commands[:commandIndex + 1]
				,message.discord_py.channel
			) == False
		):
			#Stops the loop if the user does not have permission for this command.
			
			await self.useDenied(message, commandCall, commandIndex)
			return
		
		await self.checkSubCommands(message, callIndex, commandIndex)
	
	async def checkOwnerOnly(self, message):
		if (self.owner_only == True):
			ownerId = await getCsvVar("OWNER_ID", "basic", "staticData")
			return message.discord_py.author.id == int(ownerId)
		
		return True
	
	async def checkSubCommands(self, message, callIndex, commandIndex):
		commandCall = message.calls[callIndex]
		
		if (commandIndex != -1):
			commandCode = commandCall.commands[commandIndex]
		else:
			commandCode = None
		
		nextCommandIndex = commandIndex + 1
		if (nextCommandIndex < len(commandCall.commands)):
			nextCommandCode = commandCall.commands[nextCommandIndex]
		else:
			nextCommandCode = None
		
		#If there are more commands in the call.
		if (nextCommandIndex < len(commandCall.commands)):
			if (nextCommandCode in self.sub_commands):
				await self.sub_commands[nextCommandCode].call(message, callIndex, commandIndex + 1)
			else:
				if (len(self.sub_commands) == 0):
					msg = await self.getSimpleHelp(message, commandCall, commandIndex)
					await send(message.discord_py.channel, msg)
				else:
					#If the command was wrong.
					await self.displaySubCommands(message, commandCall, commandIndex)
			
			return
		
		#If the command has sub-commands but none were given...
		if (len(self.sub_commands) > 0):
			await self.displaySubCommands(message, commandCall, commandIndex)
			return
		
		#If right amount of arguments were not given.
		if (await self.validateArgumentCount(len(commandCall.arguments)) == False):
			msg = await self.getSimpleHelp(message, commandCall, commandIndex)
			await send(message.discord_py.channel, msg)
			return
		
		#Converting all the arguments to the proper data types. Returns True if successful.
		errorMsg = await commandCall.convertArguments(self, message.language)
		
		if (errorMsg == ""):
			await self.launchCommand(message, commandCall.arguments)
		else:
			errorMsg += await self.getSimpleHelp(message, await commandCall.command_string)
			await send(message.discord_py.channel, errorMsg)
	
	#Procedures involving command launching.
	#Checks for NSFW functions, too.
	async def launchCommand(self, message, arguments):
		#If an ordinary channel, normal function is executed.
		#If there is no normal function, the command is blocked.
		if (message.discord_py.channel.is_nsfw() == False):
			if (self.function != None):
				await self.function(message, arguments)
			else:
				await send(
					message.discord_py.channel
					,await getLanguageText(
						message.language
						,"NSFW_COMMAND"
					)
				)
		
		#If an NSFW channel, the NSFW function is executed.
		#If NSFW function does not exist, normal function is executed.
		else:
			if (self.nsfw_function == None):
				await self.function(message, arguments)
			else:
				await self.nsfw_function(message, arguments)
	
	async def validateArgumentCount(self, argumentCount):
		minArgumentCount = len(self.argument_types)
		
		if (argumentCount == minArgumentCount):
			return True
		
		if (argumentCount > minArgumentCount and self.optional_arguments_type != None):
			return True
		
		return False
	
	async def displaySubCommands(self, message, commandCall, commandIndex):
		#Used when an incomplete command gets typed.
		prefix = await Prefix(message).getPrefix()
		await commandCall.trimCommandStrings(commandIndex)
		commandStr = await commandCall.getCommandString()
		
		if (commandStr != ""):
			commandStr += "."
		
		commandStr = prefix + commandStr
		subCommands = []
		
		for key in self.sub_commands:
			sub_command = self.sub_commands[key]
			
			subCmdName = await getCommandName(message.language, sub_command.name, commandCall.commands)
			subCmdDesc = await getLanguageText(message.language, sub_command.short_desc)
			
			subCmdStr = commandStr + subCmdName + " - " + subCmdDesc
			subCommands.append(subCmdStr)
		
		msg = ""
		for subCommand in subCommands:
			msg += "```" + subCommand + "```"
		
		await send(message.discord_py.channel, msg)
	
	#Shows a simple syntax of the command, and displays the long description.
	#Informs the user about what is needed for the command.
	async def getSimpleHelp(self, message, commandCall, commandIndex):
		commandStr = await commandCall.getTrimmedCommandString(message, commandIndex)
		argumentStr = await getLanguageText(message.language, self.argument_help)
		desc = await self.getLongDesc(message.language)
		
		if (argumentStr != ""):
			argumentStr = " [" + argumentStr + "]"
		else:
			argumentStr = ""
		
		msg = "```" + commandStr + argumentStr + "```" + desc
		return msg
	
	async def useDenied(self, message, commandCall, commandIndex):
		#Called when a user is not allowed to use a command.
		commandStr = await commandCall.getTrimmedCommandString(message, commandIndex)
		
		msg = await getLanguageText(message.language, "USE_DENIED")
		msg = msg.format(command=commandStr)
		
		await send(message.discord_py.channel, msg)
	
	async def getLongDesc(self, language):
		existingLanguages = await getExistingLanguages(language)
		languagesString = "\n".join(existingLanguages)
		
		try:
			desc = await readTextFile(self.long_desc, "languages\\" + language + "\\descriptions")
			desc = desc.format(languages=languagesString)
		except FileNotFoundError:
			desc = await getLanguageText(language, self.short_desc)
		
		return desc