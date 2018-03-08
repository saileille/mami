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
	):
		self.language = language
		self.prefix = prefix
		self.shortcuts = shortcuts
		self.lists = lists
		self.autoresponses = autoresponses
	
	async def isDefault(self):
		#Checks if the Server object is the default one.
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
		
		return True