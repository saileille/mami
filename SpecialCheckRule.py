from fileIO import getLanguageText
from sendFunctions import processMsg
from specialCheckFunctions import *

class SpecialCheckRule(object):
	format_strings = {
		"min_players": "message.channel_settings.quiz.min_players"
		,"player": "message.channel_settings.quiz.players[message.discord_py.author.id].name"
	}
	
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
	
	#Returns None if the check goes through, otherwise returns error message.
	async def preCheck(self, message):
		if (self.pre_check == None):
			return None
		
		if (await self.pre_check(message) == True):
			return None
		
		return await processMsg(
			self.description
			,message.language
			,await self.processFormatting(message)
		)
	
	async def postCheck(self, message):
		if (self.post_check == None):
			return True
		
		return await self.post_check(message)
	
	async def processFormatting(self, message):
		processedFormatting = {}
		
		for key in self.format_strings:
			try:
				processedFormatting[key] = eval(self.format_strings[key])
			except (AttributeError, KeyError) as e:
				processedFormatting[key] = None
		
		return processedFormatting