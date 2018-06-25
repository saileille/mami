class SpecialCheckRule(object):
	def __init__(
		self
		,pre_check = None
		,post_check = None
		,description = None
	):
		#pre_check: applies to everyone.
		#post_check: applies only to those who would not have a permission otherwise.
		
		self.pre_check = pre_check
		self.post_check = post_check
		self.description = description