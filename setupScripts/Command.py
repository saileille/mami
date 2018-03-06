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