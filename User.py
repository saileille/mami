from SettingObject import SettingObject

from bot import client
from fileIO import getDefaultLanguage

class User(SettingObject):
	def __init__(
		self
		,language = None
		,prefix = None
		,rpg_character = None
	):
		super().__init__(
			language
			,prefix
		)
		self.rpg_character = rpg_character
	
	#Checks if the User object is the default one.
	async def isDefault(self):
		if (self.language != await getDefaultLanguage()):
			return False
		
		if (self.prefix != None):
			return False
		
		if (self.rpg_character != None):
			return False
		
		return True
	
	async def forceDefault(self):
		self.language = None
		self.prefix = None
		self.rpg_character = None
	
	#Returns a boolean indicating whether the user exists.
	async def isValid(self, id):
		return bool(client.get_user(id))