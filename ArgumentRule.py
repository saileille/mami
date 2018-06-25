#A class determining what kind of arguments are allowed.

import re

from fileIO import getCharacterLimit

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
		
		#Strings which are evalled when needed.
		self.num_range = num_range
	
	async def checkArgument(self, argument):
		result = re.fullmatch(self.pattern, argument)
		
		return bool(result)
	
	async def convertArgument(self, argument):
		try:
			if (self.conversion == "int"):
				try:
					argument = int(argument)
				
				#Cannot convert straight to int from string representation of float.
				except ValueError:
					argument = float(argument)
					argument = int(argument)
			
			elif (self.conversion == "float"):
				argument = float(argument)
		
		except ValueError:
			return None
		
		return argument
	
	async def checkRange(self, argument):
		if (self.num_range == None):
			return True
		
		characterLimit = await getCharacterLimit()
		
		evalRange = []
		for item in self.num_range:
			evalItem = eval(item)
			print(repr(evalItem))
			evalRange.append(evalItem)
		
		return (
			argument >= evalRange[0]
			and argument <= evalRange[1]
		)