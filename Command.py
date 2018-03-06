class Command(object):
	def __init__(
		self
		,name = ""
		,short_desc = ""
		,long_desc = ""
		,sub_commands = []
		,hidden = False
		,owner_only = False
		,function = None
	):
		self.name = name
		self.short_desc = short_desc
		self.long_desc = long_desc
		self.sub_commands = sub_commands
		self.hidden = hidden
		self.owner_only = owner_only
		self.function = function
	
	async def call(self, message, callIndex):
		if (await self.checkOwnerOnly(message) == False):
			#TODO: function to inform the user of the inability to use this command.
			return
		
		
	
	async def checkOwnerOnly(self, message):
		from fileIO import getCsvVar
		
		if (self.owner_only == True):
			ownerId = await getCsvVar("OWNER_ID", "basic", "staticData")
			
			return message.discord_py.author.id == ownerId
		
		return True