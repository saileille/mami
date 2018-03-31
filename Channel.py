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
	
	async def getPermissionsPerCommand(self, permissionDict, channelID):
		#Assigns the permissions to the dictionary.
		#This function is slightly different for server.
		
		for key in self.permissions:
			if (key not in permissionDict):
				permissionDict[key] = {}
			
			if ("channels" not in permissionDict[key]):
				permissionDict[key]["channels"] = {}
			
			permissionDict[key]["channels"][channelID] = self.permissions[key]