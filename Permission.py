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
	
	async def isDefault(self):
		#Checks if the Permission object is the default one.
		
		if (len(self.users) > 0):
			return False
		
		if (len(self.roles) > 0):
			return False
		
		if (len(self.permissions) > 0):
			return False
		
		return True
	
	async def checkPermission(self, user, userPermissions):
		#Checks for the user ID.
		allowed = await self.checkUserId(user.id)
		
		if (allowed == True or allowed == False):
			return allowed
		
		#Checks for the role IDs.
		allowed = await self.checkRoleIds(user.roles)
		
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
		"""
		for role in roles:
			print("{number}: {name}".format(number=role.position, name=role.name))
		"""
		
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