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