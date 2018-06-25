#Contains all variables that may be thrown in a message.
class MessageVariables(object):
	def __init__(self):
		self.argument = ""
		self.bot_name = ""
		self.channel_synclist = ""
		self.command = ""
		self.id = ""
		self.language = ""
		self.languages = ""
		self.min_players = ""
		self.name = ""
		self.participants = ""
		self.player = ""
		self.players = ""
		self.prefix = ""
		self.user = ""
		self.winners = ""
	
	async def implement(self, msg, varDict):
		return
	
	async def initialise(self, varDict):
		if ("argument" in varDict):
			self.argument = varDict["argument"]
		
		