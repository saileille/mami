#A user playing in a quiz.

class QuizPlayer(object):
	def __init__(self, guildMember):
		self.id = guildMember.id
		self.name = guildMember.display_name
		self.points = 0
		self.active = True
	
	#Returns a string used in quiz standings.
	async def getStandingsString(self, rank):
		return "{rank}. {name} - {points:.2f}".format(
			rank = rank
			,name = self.name
			,points = self.points
		)