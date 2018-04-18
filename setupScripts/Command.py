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
		,optional_arguments_type = None
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
		self.optional_arguments_type = optional_arguments_type
		self.default_permissions = default_permissions
		self.function = function
	
	def getDict(self):
		dictionary = {}
		
		if (self.name != "head"):
			#Emits the top layer code.
			dictionary["name"] = ""
		
		dictionary["sub_commands"] = {}
		
		#Returns a dictionary of the object.
		for sub_command in self.sub_commands:
			dictionary["sub_commands"][sub_command.name] = sub_command.getDict()
		
		return dictionary