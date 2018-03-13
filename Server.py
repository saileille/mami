class Server(object):
	from fileIO import getCsvVarSync
	
	defaultLanguage = getCsvVarSync("DEFAULT_LANGUAGE", "basic", "staticData")
	
	def __init__(
		self
		,language = defaultLanguage
		,prefix = None
		,shortcuts = {}
		,lists = {}
		,autoresponses = {}
		,permissions = {}
	):
		self.language = language
		self.prefix = prefix
		self.shortcuts = shortcuts
		self.lists = lists
		self.autoresponses = autoresponses
		self.permissions = permissions
	
	async def isDefault(self):
		#Checks if the Server object is the default one.
		
		await self.cleanPermissions()
		
		if (self.language != self.defaultLanguage):
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
	
	async def cleanPermissions(self):
		deleteKeys = []
		for key in self.permissions:
			if (await self.permissions[key].isDefault() == True):
				deleteKeys.append(key)
		
		for key in deleteKeys:
			del self.permissions[key]
	
	async def save(self, message):
		from fileIO import savePickle
		from fileIO import deleteFile
		
		#await self.cleanPermissions()
		
		folder = "savedData\\servers"
		await savePickle(self, message.server.id, folder)