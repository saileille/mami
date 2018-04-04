from fileIO import getLanguageText

#Class to keep track of command permissions.

class Permission(object):
	def __init__(
		self
		,users = {}
		,roles = {}
		,permissions = []
	):
		self.users = users
		self.roles = roles
		self.permissions = permissions
	
	async def isDefault(self, cmdPermissions):
		#Checks if the Permission object is the default one.
		
		if (len(self.users) > 0):
			return False
		
		if (len(self.roles) > 0):
			return False
		
		if (await self.defaultCommandPermissions(cmdPermissions) == False):
			return False
		
		return True
	
	async def forceDefault(self):
		#Converts the object to its default state.
		self.users = {}
		self.roles = {}
		self.permissions = []
	
	async def defaultCommandPermissions(self, cmdPermissions):
		#Checks if the permission list is the default one.
		if (len(cmdPermissions) == len(self.permissions)):
			for permission in self.permissions:
				if (permission not in cmdPermissions):
					return False
			
			return True
		
		return False
	
	async def checkPermission(self, user, userPermissions):
		#Checks for the user ID.
		allowed = await self.checkUserId(user.id)
		
		if (allowed == True or allowed == False):
			return allowed
		
		#Checks for the role IDs.
		#Inside try-except in case of command being executed in DMs.
		try:
			allowed = await self.checkRoleIds(user.roles)
		except AttributeError:
			pass
		
		if (allowed == True or allowed == False):
			return allowed
		
		return await self.checkPermissionNames(userPermissions)
	
	async def toDict(self):
		return self.__dict__
	
	async def checkUserId(self, id):
		#True = User is allowed to use the command.
		#False = User is not allowed to use the command.
		#None = Undecided. Further checks are needed.
		
		if (len(self.users) == 0):
			#The list is void of IDs.
			return None
		
		if (id in self.users):
			#The ID was found among the user IDs.
			if (self.users[id] == "allow"):
				return True
			
			return False
		
		if (await self.checkAllowed(self.users) == True):
			#There are only allowed IDs in the list.
			return False
		
		#Permission cannot be determined - checking roles next.
		return None
	
	async def checkRoleIds(self, roles):
		#True = User is allowed to use the command.
		#False = User is not allowed to use the command.
		#None = Undecided. Further checks are needed.
		
		if (len(self.roles) == 0):
			#The list is void of IDs.
			return None
		
		roles.sort(key=lambda role: role.position, reverse=True)
		
		for role in roles:
			#The ID was found among the user IDs.
			if (role.id in self.roles):
				if (self.roles[role.id] == "allow"):
					return True
				
				return False
		
		if (await self.checkAllowed(self.roles) == True):
			#There are only allowed IDs in the list.
			return False
		
		#Permission cannot be determined - checking permissions next.
		return None
	
	async def checkPermissionNames(self, userPermissions):
		#True = User is allowed to use the command.
		#False = User is not allowed to use the command.
		
		#Checks if ALL given permission names are found from the user.
		for permission in self.permissions:
			if (eval("userPermissions." + permission + " == False")):
				return False
		
		return True
	
	async def checkAllowed(self, dictionary):
		#Checks if all the dictionary IDs have "allow" as value.
		
		allAllowed = True
		for key in dictionary:
			if (dictionary[key] == "deny"):
				allAllowed = False
				break
		
		return allAllowed
	
	async def getPermissionString(self, discordMessage, language):
		#Gives a human-readable representation of who can use the command.
		#Returns a list, use StringHandler object for chapter divide.
		stringList = []
		stringList += await self.getPermissionStringUsers(discordMessage, language)
		stringList += await self.getPermissionStringRoles(discordMessage, language)
		stringList += await self.getPermissionStringPermissions(language)
		
		if (len(stringList) == 0):
			stringList.append(await getLanguageText(language, "NO_PERMISSIONS"))
		
		return stringList
	
	async def getPermissionStringUsers(self, discordMessage, language):
		stringList = []
		allowed = []
		blocked = []
		
		for id in self.users:
			member = discordMessage.server.get_member(id)
			
			if (member != None):
				name = member.display_name
			else:
				name = "[undefined]"
			
			memberDict = {
				"name": name
				,"id": id
			}
			
			if (self.users[id] == "allow"):
				allowed.append(memberDict)
			else:
				blocked.append(memberDict)
		
		
		if (len(allowed) > 0):
			string = await getLanguageText(language, "PERMISSION.USERS_ALLOWED")
			
			for user in allowed:
				string += "\n - {name} ({id})".format(name=user["name"], id=user["id"])
			
			stringList.append(string)
		
		if (len(blocked) > 0):
			string = await getLanguageText(language, "PERMISSION.USERS_BLOCKED")
			
			for user in blocked:
				string += "\n - {name} ({id})".format(name=user["name"], id=user["id"])
			
			stringList.append(string)
		
		return stringList
	
	async def getPermissionStringRoles(self, discordMessage, language):
		stringList = []
		allowed = []
		blocked = []
		
		for id in self.roles:
			for role in discordMessage.server.roles:
				if (id == role.id):
					roleDict = {"name": role.name}
					break
			else:
				roleDict = {"name": "[undefined]"}
			
			roleDict["id"] = id
			
			if (self.roles[id] == "allow"):
				allowed.append(roleDict)
			else:
				blocked.append(roleDict)
		
		if (len(allowed) > 0):
			string = await getLanguageText(language, "PERMISSION.ROLES_ALLOWED")
			
			for role in allowed:
				string += "\n - {name} ({id})".format(name=role["name"], id=role["id"])
			
			stringList.append(string)
		
		if (len(blocked) > 0):
			string = await getLanguageText(language, "PERMISSION.ROLES_BLOCKED")
			
			for role in blocked:
				string += "\n - {name} ({id})".format(name=role["name"], id=role["id"])
			
			stringList.append(string)
		
		return stringList
	
	async def getPermissionStringPermissions(self, language):
		stringList = []
		
		if (len(self.permissions) > 0):
			string = await getLanguageText(language, "PERMISSION.PERMISSIONS_ALLOWED")
			
			for permission in self.permissions:
				string += "\n" + permission
			
			stringList.append(string)
		
		return stringList