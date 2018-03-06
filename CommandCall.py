class CommandCall(object):
	from fileIO import getCsvVarSync
	
	defaultPrefix = getCsvVarSync("DEFAULT_PREFIX", "basic", "staticData")
	
	def __init__(
		self
		,raw_text = ""
	):
		self.raw_text = raw_text
		self.prefix = None
		self.commands = []
		self.arguments = []
	
	async def process(self, customPrefix):
		#Sorts the command calls appropriately.
		if (self.raw_text.startswith(self.defaultPrefix)):
			await self.trimPrefix(len(self.defaultPrefix))
		elif (self.raw_text.startswith(customPrefix)):
			await self.trimPrefix(len(customPrefix))
		else:
			#No prefix, no fun.
			self.arguments = None
			self.commands = None
			return
		
		await self.parse()
	
	async def trimPrefix(self, prefixLength):
		self.raw_text = self.raw_text[prefixLength:]
	
	async def parse(self):
		#Gives command list and argument list.
		parts = self.raw_text.split(" ")
		self.arguments = parts[1:]
		
		commandParts = parts[0].split(".")
		self.commands = commandParts