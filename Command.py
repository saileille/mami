from bot import send
from commandFunctions import commandNotFound
from fileIO import getCommandName
from fileIO import getCsvVar
from fileIO import getLanguageCode
from fileIO import getLanguageText
from Permission import Permission
from Prefix import Prefix

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
		,default_permissions = []
		,function = None
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
		self.default_permissions = default_permissions
		self.function = function
	
	async def call(self, message, callIndex, commandIndex):
		commandCall = message.calls[callIndex]
		
		if (await commandCall.validatePrefix(message, self.all_prefixes) == False):
			#Validating the prefix. Execution will not continue if invalid.
			return
		
		if (await self.checkOwnerOnly(message) == False):
			#TODO: function to inform the user of the inability to use this command.
			return
		
		if (commandIndex != -1
			and await self.getPermission(message, commandCall, commandIndex) == False):
			
			#Stops the loop if the user does not have permission for this command.
			
			await self.useDenied(message, commandCall, commandIndex)
			return
		
		await self.checkSubCommands(message, callIndex, commandIndex)
	
	async def checkOwnerOnly(self, message):
		if (self.owner_only == True):
			ownerId = await getCsvVar("OWNER_ID", "basic", "staticData")
			return message.discord_py.author.id == ownerId
		
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
		
		if (nextCommandIndex < len(commandCall.commands)):
			#If there are more commands in the call.
			
			if (nextCommandCode in self.sub_commands):
				await self.sub_commands[nextCommandCode].call(message, callIndex, commandIndex + 1)
			else:
				#await commandNotFound(self, await commandCall.getCommandString())
				
				if (len(self.sub_commands) == 0):
					msg = await self.getSimpleHelp(message, commandCall, commandIndex)
					await send(message.discord_py.channel, msg)
				else:
					#If the command was wrong.
					await self.displaySubCommands(message, commandCall, commandIndex)
			
			return
		
		if (len(self.sub_commands) > 0):
			#If the command has sub-commands but none were used...
			await self.displaySubCommands(message, commandCall, commandIndex)
			return
		
		if (len(commandCall.arguments) < len(self.argument_types)):
			#If not enough arguments were given.
			msg = await self.getSimpleHelp(message, commandCall, commandIndex)
			await send(message.discord_py.channel, msg)
			return
		
		#Converting all the arguments to the proper data types. Returns True if successful.
		errorMsg = await commandCall.convertArguments(self, await message.getLanguage())
		
		if (errorMsg == ""):
			await self.function(message, commandCall.arguments)
		else:
			errorMsg += await self.getSimpleHelp(message, await commandCall.command_string)
			await send(message.discord_py.channel, errorMsg)
	
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
			
			subCmdName = await getCommandName(await message.getLanguage(), sub_command.name, commandCall.commands)
			subCmdDesc = await getLanguageText(await message.getLanguage(), sub_command.short_desc)
			
			subCmdStr = commandStr + subCmdName + " - " + subCmdDesc
			subCommands.append(subCmdStr)
		
		msg = "```"
		
		for subCommand in subCommands:
			msg += "\n" + subCommand
		
		msg += "```"
		await send(message.discord_py.channel, msg)
	
	async def getSimpleHelp(self, message, commandCall, commandIndex):
		#Shows a simple syntax of the command, and displays the short description.
		#Informs the user about what is needed for the command.
		
		commandStr = await commandCall.getTrimmedCommandString(message, commandIndex)
		argumentStr = await getLanguageText(await message.getLanguage(), self.argument_help)
		shortDesc = await getLanguageText(await message.getLanguage(), self.short_desc)
		
		if (argumentStr != ""):
			argumentStr = " [" + argumentStr + "]"
		else:
			argumentStr = ""
		
		msg = "```" + commandStr + argumentStr + "```" + shortDesc
		return msg
	
	async def getPermission(self, message, commandCall, commandIndex):
		userPermissions = message.discord_py.author.permissions_in(message.discord_py.channel)
		
		#Admins get past everything.
		"""
		if (userPermissions.administrator == True):
			return True
		"""
		
		commandList = commandCall.commands[:commandIndex + 1]
		permissionKey = ".".join(commandList)
		
		#Adds a default Permission object if the command is lacking one for this server.
		if (permissionKey not in message.server_settings.permissions):
			message.server_settings.permissions[permissionKey] = Permission(
				permissions = self.default_permissions
			)
			
			await message.server_settings.save(message)
		
		"""
		if (await self.noGivenPermissions(message, permissionKey)):
			#No given permissions.
			for defaultPermission in self.default_permissions:
				if (eval("userPermissions." + defaultPermission + " == False")):
					return False
			
			return True
		"""
		
		permission = message.server_settings.permissions[permissionKey]
		
		print(await permission.toDict())
		#Checking server-wide permissions (channel-specific permissions should come before).
		return await permission.checkPermission(message.discord_py.author, userPermissions)
	
	async def useDenied(self, message, commandCall, commandIndex):
		#Called when a user is not allowed to use a command.
		commandStr = await commandCall.getTrimmedCommandString(message, commandIndex)
		
		msg = await getLanguageText(await message.getLanguage(), "COMMAND.USE_DENIED")
		msg = msg.format(command=commandStr)
		
		await send(message.discord_py.channel, msg)
	
	"""
	async def noGivenPermissions(self, message, permissionKey):
		#Checks if the command has user-given permissions.
		return (
			(
				permissionKey in message.server_settings.permissions
				and await message.server_settings.permissions[permissionKey].isDefault() == True
			) or
			permissionKey not in message.server_settings.permissions
		)
	"""