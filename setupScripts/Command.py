class Command(object):
	def __init__(
		self
		,name = ""
		,sub_commands = []
		,hidden = False
		,owner_only = False
		,server_only = False
		,all_prefixes = False
		,delete_message = False
		,argument_types = []
		,optional_arguments_type = None
		,default_permissions = []
		,special_checks = []
		,function = None
		,nsfw_function = None
	):
		self.name = name
		self.sub_commands = sub_commands
		self.hidden = hidden
		self.owner_only = owner_only
		self.server_only = server_only
		self.all_prefixes = all_prefixes
		self.delete_message = delete_message
		self.argument_types = argument_types
		self.optional_arguments_type = optional_arguments_type
		self.default_permissions = default_permissions
		self.special_checks = special_checks
		self.function = function
		self.nsfw_function = nsfw_function
		self.command_code = None
		self.short_desc = None
		self.argument_help = None
	
	def getDict(self):
		dictionary = {}
		
		#Emits the top layer code.
		if (self.name != "head"):
			dictionary["name"] = ""
		
		dictionary["sub_commands"] = {}
		
		#Returns a dictionary of the object.
		for sub_command in self.sub_commands:
			dictionary["sub_commands"][sub_command.name] = sub_command.getDict()
		
		return dictionary