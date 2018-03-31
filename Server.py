from fileIO import getCsvVarSync
from StringHandler import StringHandler

#Server settings and configuration class.

class Server(object):
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
	
	async def forceDefault(self):
		#Forces the object to its default values.
		self.language = self.defaultLanguage
		self.prefix = None
		self.shortcuts = {}
		self.lists = {}
		self.autoresponses = {}
		self.permissions = {}
	
	async def cleanPermissions(self):
		deleteKeys = []
		for key in self.permissions:
			cmdObject = await StringHandler(key).getCommandFromString()
			
			if (await self.permissions[key].isDefault(cmdObject.default_permissions) == True):
				deleteKeys.append(key)
		
		for key in deleteKeys:
			del self.permissions[key]
	
	async def deletePermissions(self, commandCodes):
		#Deletes the given permission keys.
		
		for key in commandCodes:
			if (key in self.permissions):
				del self.permissions[key]
	
	async def getPermissionsPerCommand(self, permissionDict):
		#Assigns the permissions to the dictionary.
		#This function is slightly different for channel.
		
		for key in self.permissions:
			if (key not in permissionDict):
				permissionDict[key] = {}
			
			permissionDict[key]["server"] = self.permissions[key]