from copy import deepcopy
from discord import DMChannel

from CommandCall import CommandCall
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
		,sub_commands = {}
		,hidden = False
		,owner_only = False
		,server_only = False
		,all_prefixes = False
		,delete_message = False
		,argument_types = []
		,optional_arguments_type = None
		,default_permissions = []
		,function = None
		,nsfw_function = None
	):
		self.name = name
		self.sub_commands = sub_commands
		self.hidden = hidden
		self.owner_only = owner_only
		self.server_only = server_only
		self.all_prefixes = all_prefixes
		self.delete_message = delete_message
		self.argument_types = argument_types
		self.optional_arguments_type = optional_arguments_type
		self.default_permissions = default_permissions
		self.function = function
		self.nsfw_function = nsfw_function
		self.command_code = None
		self.short_desc = None
		self.argument_help = None
	
	async def call(self, message, callIndex, commandIndex):
		if (self.delete_message == True):
			await message.discord_py.delete()
		
		commandCall = message.calls[callIndex]
		
		if (await self.permissionChecklist(message, commandCall, commandIndex) == True):
			await self.checkSubCommands(message, callIndex, commandIndex)
	
	#ALL permission checks put to one function.
	#sendFeedback enables/disables feedback messages.
	async def permissionChecklist(self, message, commandCall, commandIndex, sendFeedback=True):
		#Validating the prefix. Execution will not continue if invalid.
		if (await commandCall.validatePrefix(message, self.all_prefixes) == False):
			return False
		
		#TODO: function to inform the user of the inability to use this command.
		if (await self.checkOwnerOnly(message, sendFeedback) == False):
			return False
		
		if (await self.checkServerOnly(message, sendFeedback) == False):
			return False
		
		#Checks for the command permissions.
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
			if (sendFeedback == True):
				await self.sendUseDenied(message, commandCall, commandIndex)
			
			return False
		
		if (await self.checkNsfw(message, sendFeedback) == False):
			return False
		
		return True
	
	async def checkOwnerOnly(self, message, sendFeedback):
		if (self.owner_only == False):
			return True
		
		ownerId = await getCsvVar("OWNER_ID", "basic", "staticData")
		returnValue = message.discord_py.author.id == int(ownerId)
		
		if (returnValue == False and sendFeedback == True):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "OWNER_ONLY_COMMAND")
			)
		
		return returnValue
	
	async def checkServerOnly(self, message, sendFeedback):
		if (self.server_only == False):
			return True
		
		returnValue = isinstance(message.discord_py.channel, DMChannel) == False
		
		if (returnValue == False and sendFeedback == True):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "SERVER_ONLY_COMMAND")
			)
		
		return returnValue
	
	async def checkNsfw(self, message, sendFeedback):
		#The sub-command length must be checked, otherwise the check fails at self.function.
		returnValue = (
			isinstance(message.discord_py.channel, DMChannel)
			or message.discord_py.channel.is_nsfw()
			or len(self.sub_commands) > 0
			or self.function != None
		)
		
		if (returnValue == False and sendFeedback == True):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "NSFW_NOT_ALLOWED")
			)
		
		return returnValue
	
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
			errorMsg += await self.getSimpleHelp(message, commandCall, commandIndex)
			await send(message.discord_py.channel, errorMsg)
	
	#Procedures involving command launching.
	#Checks for NSFW functions, too.
	async def launchCommand(self, message, arguments):
		#If a private channel, the safe-for-work functionality takes priority.
		#Exclusively NSFW commands are not blocked, though.
		if (isinstance(message.discord_py.channel, DMChannel) == True):
			if (self.function != None):
				await self.function(message, arguments)
			else:
				await self.nsfw_function(message, arguments)
			
			return
		
		#If an ordinary channel, normal function is executed.
		#If there is no normal function, the command is blocked.
		if (message.discord_py.channel.is_nsfw() == False):
			if (self.function != None):
				await self.function(message, arguments)
			
			return
		
		#If an NSFW channel, the NSFW function is executed.
		#If NSFW function does not exist, normal function is executed.
		if (self.nsfw_function != None):
			await self.nsfw_function(message, arguments)
		else:
			await self.function(message, arguments)
	
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
		previousCommand = await commandCall.getCommandString()
		
		commandStr = previousCommand
		if (commandStr != ""):
			commandStr += "."
		
		commandStr = prefix + commandStr
		previousCommand = prefix + previousCommand
		
		subCommands = []
		for key in self.sub_commands:
			sub_command = self.sub_commands[key]
			
			permissionCall = deepcopy(commandCall)
			permissionCall.commands += [key]
			permissionIndex = commandIndex + 1
			
			if (permissionCall.commands[0] == None):
				permissionCall.commands = permissionCall.commands[1:]
			
			if (await sub_command.permissionChecklist(message, permissionCall, permissionIndex, sendFeedback=False) == True):
			
				subCmdName = await getCommandName(message.language, sub_command.name, commandCall.commands)
				subCmdDesc = await getLanguageText(message.language, sub_command.short_desc)
				
				subCmdStr = commandStr + subCmdName + " - " + subCmdDesc
				subCommands.append(subCmdStr)
		
		msg = ""
		for subCommand in subCommands:
			msg += "```" + subCommand + "```"
		
		if (msg == ""):
			msg = await getLanguageText(message.language, "NO_AVAILABLE_COMMANDS")
			msg = msg.format(command=previousCommand)
		
		await send(message.discord_py.channel, msg)
	
	#Shows a simple syntax of the command, and displays the long description.
	#Informs the user about what is needed for the command.
	async def getSimpleHelp(self, message, commandCall, commandIndex):
		commandStr = await commandCall.getTrimmedCommandString(message, commandIndex)
		argumentStr = await getLanguageText(message.language, self.argument_help)
		desc = await self.getLongDesc(message.language)
		
		if (argumentStr != ""):
			argumentStr = " " + argumentStr
		else:
			argumentStr = ""
		
		msg = "```" + commandStr + argumentStr + "```" + desc
		return msg
	
	#Called when a user is not allowed to use a command.
	async def sendUseDenied(self, message, commandCall, commandIndex):
		commandStr = await commandCall.getTrimmedCommandString(message, commandIndex)
		
		msg = await getLanguageText(message.language, "USE_DENIED")
		msg = msg.format(command=commandStr)
		
		await send(message.discord_py.channel, msg)
	
	async def getLongDesc(self, language):
		existingLanguages = await getExistingLanguages(language)
		languagesString = "\n".join(existingLanguages)
		
		try:
			desc = await readTextFile(self.command_code, "languages\\" + language + "\\descriptions")
			desc = desc.format(languages=languagesString)
		except FileNotFoundError:
			desc = await getLanguageText(language, self.short_desc)
		
		return desc