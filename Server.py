from SettingObject import SettingObject
from StringHandler import StringHandler

from bot import client
from fileIO import getCsvVarSync
from fileIO import getDefaultLanguage

#Server settings and configuration class.
class Server(SettingObject):
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
		)
		self.shortcuts = shortcuts
		self.lists = lists
		self.autoresponses = autoresponses
		self.permissions = permissions
	
	#Checks if the Server object is the default one.
	async def isDefault(self):
		await self.cleanPermissions()
		
		if (
			self.language != await getDefaultLanguage()
			and self.language != None
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
	
	#Forces the object to its default values.
	async def forceDefault(self):
		self.language = None
		self.prefix = None
		self.shortcuts = {}
		self.lists = {}
		self.autoresponses = {}
		self.permissions = {}
	
	#Returns a boolean indicating whether the server exists.
	async def isValid(self, id):
		return bool(client.get_guild(id))
	
	async def cleanPermissions(self):
		deleteKeys = []
		for key in self.permissions:
			cmdObject = await StringHandler(key).getCommandFromString()
			
			if (await self.permissions[key].isDefault(cmdObject.default_permissions) == True):
				deleteKeys.append(key)
		
		for key in deleteKeys:
			del self.permissions[key]
	
	#Deletes the given permission keys.
	async def deletePermissions(self, commandCodes):
		for key in commandCodes:
			if (key in self.permissions):
				del self.permissions[key]
	
	#Assigns the permissions to the dictionary.
	#This function is slightly different for channel.
	async def getPermissionsPerCommand(self, permissionDict):
		for key in self.permissions:
			if (key not in permissionDict):
				permissionDict[key] = {}
			
			permissionDict[key]["server"] = self.permissions[key]