#A class determining what kind of arguments are allowed.

class ArgumentRule(object):
	def __init__(
		self
		,pattern = ".*"
		,conversion = ""
		,fail_description = "!"
		,num_range = None
	):
		self.pattern = pattern
		self.conversion = conversion
		self.fail_description = fail_description
		self.num_range = num_range