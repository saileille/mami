import copy

from bot import send
from fileIO import getPermissions
from Permission import Permission
from StringHandler import StringHandler

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
		await self.parseArguments()
		
		if (self.valid_change == False):
			return
		
		#print(self.__dict__)
		await self.updatePermissions(message, settingObject)
	
	async def parseArguments(self):
		#Handles commands, user tags, etc. and returns success as a boolean.
		
		await self.parseCommands()
		
		if (self.valid_change == False):
			#TODO: Message to inform the user of the faulty input.
			return
		
		await self.parseMentions()
	
	async def parseCommands(self):
		#Looping through arguments, getting valid commands.
		for i in range(len(self.arguments)):
			stringHandler = StringHandler(self.arguments[i])
			codeList = await stringHandler.getCommandCodeList(self.language)
			
			if (codeList[-1] != None):
				#Valid command lists never have None as the last item.
				codeString = ".".join(codeList)
				self.command_codes.append(codeString)
			else:
				if (self.operation != "clear"):
					#This one is not a command, thence looping is stopped.
					#Proceeding to user/role tags and permissions next.
					#Command strings are stored for later use.
					
					self.command_strings = self.arguments[:i]
					self.arguments = self.arguments[i:]
				
				break
		
		if (self.operation == "clear"):
			self.command_strings = self.arguments[:len(self.command_codes)]
		
		if (
			len(self.command_codes) == 0
			or (
				len(self.arguments) == 0
				and self.operation != "clear"
			)
		):
			#No command or argument was given.
			print("No command or argument was given")
			self.valid_change = False
	
	async def parseMentions(self):
		#Handles mentions and permission names.
		for argument in self.arguments:
			idDict = await StringHandler(argument).getIdFromMention()
			
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
			
			#If the input was not recognised.
			print("Argument " + argument + " not recognised")
			self.valid_change = False
			return
	
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
		
		msg = await StringHandler(list=msgList).getChapterDivide()
		await send(message.discord_py.channel, msg)
	
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
		print(self.permission_objects[i].__dict__)
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