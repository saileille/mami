import copy

from Permission import Permission
from StringHandler import StringHandler

from fileIO import getLanguageText
from fileIO import getPermissions
from idFunctions import isPossibleId
from sendFunctions import send

class PermissionChanger(object):
	def __init__(
		self
		,arguments = []
		,language = None
		,operation = None
	):
		self.arguments = arguments
		self.language = language
		self.operation = operation
		self.command_strings = []
		self.command_codes = []
		self.user_ids = []
		self.role_ids = []
		self.permissions = []
		self.valid_change = True
		self.permission_objects = []
	
	async def changePermissions(self, message, settingObject):
		await self.parseArguments(message)
		
		if (self.valid_change == False):
			return
		
		await self.updatePermissions(message, settingObject)
	
	async def parseArguments(self, message):
		#Handles commands, user tags, etc. and returns success as a boolean.
		
		await self.parseCommands(message)
		
		if (self.valid_change == False):
			#TODO: Message to inform the user of the faulty input.
			return
		
		await self.parseMentions(message)
	
	async def parseCommands(self, message):
		#Looping through arguments, getting valid commands.
		while (0 < len(self.arguments)):
			codeList = await StringHandler(self.arguments[0]).getCommandCodeList(self.language)
			
			#Valid command lists never have None as the last item.
			if (codeList[-1] != None):
				self.command_strings.append(self.arguments[0])
				self.arguments = self.arguments[1:]
				
				codeString = ".".join(codeList)
				self.command_codes.append(codeString)
			else:
				#This one is not a command, thence looping is stopped.
				#Proceeding to user/role tags and permissions next.
				
				#If clearing, all arguments must be commands.
				if (self.operation == "clear"):	
					await send(
						message.discord_py.channel
						,"INVALID_COMMAND"
						,message.language
						,{
							"command": self.arguments[0]
						}
					)
					self.valid_change = False
					return
				
				break
		
		#No commands...
		if (len(self.command_codes) == 0):
			msg = await getLanguageText(message.language, "INVALID_COMMAND")
			msg = msg.format(command=self.arguments[0])
			
			await send(
				message.discord_py.channel
				,"INVALID_COMMAND"
				,message.language
				,{
					"command": self.arguments[0]
				}
			)
			self.valid_change = False
			return
		
		#No arguments...
		if (len(self.arguments) == 0 and self.operation != "clear"):
			await send(
				message.discord_py.channel
				,"NO_ROLE_USER_PERMISSION_TAGS"
				,message.language
			)
			
			self.valid_change = False
			return
	
	async def parseMentions(self, message):
		#Handles mentions and permission names.
		for argument in self.arguments:
			idDict = await StringHandler(argument).getUserOrChannelId()
			
			if (idDict != None):
				if (idDict["type"] == "user"):
					self.user_ids.append(idDict["id"])
				else:
					self.role_ids.append(idDict["id"])
				
				continue
			
			permissionList = await getPermissions()
			
			if (argument in permissionList):
				self.permissions.append(argument)
				continue
			
			msg = "INVALID_ROLE_USER_PERMISSION"
			
			#If the input was not recognised.
			if (await isPossibleId(argument) == True):
				msg = "INVALID_ROLE_USER_ID"
			
			await send(
				message.discord_py.channel
				,msg
				,message.language
				,{
					"argument": argument
				}
			)
			self.valid_change = False
			break
	
	async def updatePermissions(self, message, settingObject):
		#Makes the changes to the settings object.
		msg = ""
		
		for i in range(len(self.command_codes)):
			command_code = self.command_codes[i]
			
			#The backup prevents the function from making changes to rather random commands' permissions.
			#Revert back and uncomment the permission prints to see what I mean.
			
			#permissionBackup = copy.deepcopy(settingObject.permissions)
			
			self.permission_objects.append(await self.getPermissionObject(command_code, settingObject.permissions))
			
			if (len(self.user_ids) > 0):
				if (self.operation == "undo"):
					#If removing existing permission rules.
					await self.undoUserPermissions(i)
				else:
					#If adding new permission rules.
					await self.addUserPermissions(i)
			
			if (len(self.role_ids) > 0):
				if (self.operation == "undo"):
					#If removing existing permission rules.
					await self.undoRolePermissions(i)
				else:
					#If adding new permission rules.
					await self.addRolePermissions(i)
			
			if (len(self.permissions) > 0):
				if (self.operation == "allow"):
					#Permissions can only be allowed.
					await self.addPermissionPermissions(i)
				else:
					#Trying to deny permission is the same as undoing.
					await self.undoPermissionPermissions(i)
			
			#settingObject.permissions = permissionBackup
			settingObject.permissions[command_code] = self.permission_objects[i]
		
		msgList = []
		for i in range(len(self.permission_objects)):
			msgList.append("**" + self.command_strings[i] + "**")
			msgList += await self.permission_objects[i].getPermissionString(message.discord_py, self.language)
		
		await send(
			message.discord_py.channel
			,"\n\n".join(msgList)
		)
	
	async def undoUserPermissions(self, i):
		for id in self.user_ids:
			if (id in self.permission_objects[i].users):
				del self.permission_objects[i].users[id]
	
	async def undoRolePermissions(self, i):
		for id in self.role_ids:
			if (id in self.permission_objects[i].roles):
				del self.permission_objects[i].roles[id]
	
	async def undoPermissionPermissions(self, i):
		for permissionName in self.permissions:
			self.permission_objects[i].permissions.remove(permissionName)
	
	async def addUserPermissions(self, i):
		for id in self.user_ids:
			self.permission_objects[i].users[id] = self.operation
	
	async def addRolePermissions(self, i):
		for id in self.role_ids:
			self.permission_objects[i].roles[id] = self.operation
	
	async def addPermissionPermissions(self, i):
		for permissionName in self.permissions:
			if (permissionName not in self.permission_objects[i].permissions):
				self.permission_objects[i].permissions.append(permissionName)
	
	async def getPermissionObject(self, cmdCode, permissionDict):
		#Gives a permission object, either from the dictionary, or a blank one.
		if (cmdCode in permissionDict):
			return permissionDict[cmdCode]
		
		#Gets the default permissions of the command.
		cmdObject = await StringHandler(cmdCode).getCommandFromString()
		
		permission = Permission()
		await permission.forceDefault()
		permission.permissions = cmdObject.default_permissions
		
		return permission
	
	def __str__(self):
		text = "PERMISSIONCHANGER OBJECT\n\nArguments:"
		for argument in self.arguments:
			text += "\n" + argument
		
		text += "\n\nLanguage: " + self.language
		text += "\nOperation: " + self.operation
		
		text += "\n\nCommand Strings:"
		for commandString in self.command_strings:
			text += "\n" + commandString
		
		text += "\n\nCommand Codes:"
		for commandCode in self.command_codes:
			text += "\n" + commandCode
		
		text += "\n\nUser IDs:"
		for userId in self.user_ids:
			text += "\n" + userId
		
		text += "\n\nRole IDs:"
		for roleId in self.role_ids:
			text += "\n" + roleId
		
		text += "\n\nPermissions:"
		for permission in self.permissions:
			text += "\n" + permission
		
		text += "\nValid Change: " + repr(self.valid_change)
		
		text += "\n\nPermission Objects:"
		for permissionObject in self.permission_objects:
			text += "\n" + permissionObject
		
		return text