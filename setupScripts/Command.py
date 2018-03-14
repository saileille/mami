class Command(object):
	def __init__(
		self
		,name = ""
		,short_desc = ""
		,long_desc = ""
		,sub_commands = []
		,hidden = False
		,owner_only = False
		,all_prefixes = False
		,argument_help = ""
		,argument_types = []
		,default_permissions = []
		,function = None
	):
		self.name = name
		self.short_desc = short_desc
		self.long_desc = long_desc
		self.sub_commands = sub_commands
		self.hidden = hidden
		self.owner_only = owner_only
		self.all_prefixes = all_prefixes
		self.argument_help = argument_help
		self.argument_types = argument_types
		self.default_permissions = default_permissions
		self.function = function