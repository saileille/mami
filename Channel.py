#Channel-specific configuration.

class Channel(object):
	def __init__(
		self
		,permissions = {}
	):
		self.permissions = permissions
	
	async def isDefault(self):
		#Checks if the channel is the default object.
		
		if (len(self.permissions) > 0):
			return False
		
		return True