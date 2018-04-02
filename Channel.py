from Server import Server

#Channel-specific configuration.

class Channel(Server):
	def __init__(
		self
		,language = None
		,prefix = None
		,shortcuts = {}
		,lists = {}
		,autoresponses = {}
		,permissions = {}
	):
		super().__init__(
			language
			,prefix
			,shortcuts
			,lists
			,autoresponses
			,permissions
		)
	
	#Checks if the Channel object is the default one.
	async def isDefault(self, serverLanguage):
		await self.cleanPermissions()
		
		if (
			self.language != None
			and self.language != serverLanguage
		):
			return False
		
		if (self.prefix != None):
			return False
		
		if (len(self.shortcuts) > 0):
			return False
		
		if (len(self.lists) > 0):
			return False
		
		if (len(self.autoresponses) > 0):
			return False
		
		if (len(self.permissions) > 0):
			return False
		
		return True
	
	#Assigns the permissions to the dictionary.
	#This function is slightly different for server.
	async def getPermissionsPerCommand(self, permissionDict, channelID):
		for key in self.permissions:
			if (key not in permissionDict):
				permissionDict[key] = {}
			
			if ("channels" not in permissionDict[key]):
				permissionDict[key]["channels"] = {}
			
			permissionDict[key]["channels"][channelID] = self.permissions[key]