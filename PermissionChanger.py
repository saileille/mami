class PermissionChanger(object):
	def __init__(self, arguments):
		self.arguments = arguments
		self.command_codes = []
		self.user_ids = []
		self.role_ids = []
		self.permissions = []
		self.valid_change = True
	
	async def changePermissions(self, settingObject, language, type):
		success = await self.parseArguments(language)
		
		if (success == False):
			return False
		
		print(self.__dict__)
		await self.updatePermissions(settingObject, type)
		return True
	
	async def parseArguments(self, language):
		#Handles commands, user tags, etc. and returns success as a boolean.
		await self.parseCommands(language)
		
		if (self.valid_change == False):
			#TODO: Message to inform the user of the faulty input.
			return False
		
		await self.parseMentions()
		
		if (self.valid_change == False):
			#TODO: Message to inform the user of the faulty input.
			return False
		
		return True
	
	async def parseCommands(self, language):
		from StringHandler import StringHandler
		
		#Looping through arguments, getting valid commands.
		for i in range(len(self.arguments)):
			stringHandler = StringHandler(self.arguments[i])
			codeList = await stringHandler.getCommandCodeList(language)
			
			if (codeList[-1] != None):
				#Valid command lists never have None as the last item.
				codeString = ".".join(codeList)
				self.command_codes.append(codeString)
			else:
				#This one is not a command, thence looping is stopped.
				#Proceeding to user/role tags and permissions next.
				self.arguments = self.arguments[i:]
				break
		
		if (len(self.command_codes) == 0
			or len(self.arguments) == 0):
			
			#No command or argument was given.
			print("No command or argument was given")
			self.valid_change = False
	
	async def parseMentions(self):
		#Handles permission names as well.
		
		from StringHandler import StringHandler
		from fileIO import getPermissions
		
		for argument in self.arguments:
			stringHandler = StringHandler(argument)
			idDict = await stringHandler.getIdFromMention()
			
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
	
	async def updatePermissions(self, settingObject, type):
		#Makes the changes to the settings object.
		
		from Permission import Permission
		
		for command_code in self.command_codes:
			if (command_code in settingObject.permissions):
				permission = settingObject.permissions[command_code]
			else:
				permission = Permission()
			
			if (len(self.user_ids) > 0):
				if (type == "allow" or type == "deny"):
					#If adding new permission rules.
					await self.addUserPermissions(permission, type)
				else:
					#If removing existing permission rules.
					await self.undoUserPermissions(permission)
			
			if (len(self.role_ids) > 0):
				if (type == "allow" or type == "deny"):
					#If adding new permission rules.
					await self.addRolePermissions(permission, type)
				else:
					#If removing existing permission rules.
					await self.undoRolePermissions(permission)
			
			if (len(self.permissions) > 0):
				if (type == "allow"):
					#Permissions can only be allowed, never denied.
					await self.addPermissionPermissions(permission)
				else:
					await self.undoPermissionPermissions(permission)
			
			settingObject.permissions[command_code] = permission
	
	async def undoUserPermissions(self, permission):
		for id in self.user_ids:
			if (id in permission.users):
				del permission.users[id]
	
	async def undoRolePermissions(self, permission):
		for id in self.role_ids:
			if (id in permission.roles):
				del permission.roles[id]
	
	async def undoPermissionPermissions(self, permission):
		for permissionName in self.permissions:
			permission.permissions.remove(permissionName)
	
	async def addUserPermissions(self, permission, type):
		for id in self.user_ids:
			permission.users[id] = type
	
	async def addRolePermissions(self, permission, type):
		for id in self.role_ids:
			permission.roles[id] = type
	
	async def addPermissionPermissions(self, permission):
		for permissionName in self.permissions:
			if (permissionName not in permission.permissions):
				permission.permissions.append(permissionName)