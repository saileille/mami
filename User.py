class User(object):
	from fileIO import getCsvVarSync
	
	defaultPrefix = getCsvVarSync("DEFAULT_PREFIX", "basic", "staticData")
	
	def __init__(
		self
		,prefix = defaultPrefix
		,rpg_character = None
	):
		self.prefix = prefix
		self.rpg_character = rpg_character
	
	async def isDefault(self):
		#Checks if the User object is the default one.
		if (self.prefix != self.defaultPrefix):
			return False
		
		if (self.rpg_character != None):
			return False
		
		return True