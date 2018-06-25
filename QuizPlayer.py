#A user playing in a quiz.

from TableCell import TableCell

class QuizPlayer(object):
	def __init__(self, guildMember):
		self.id = guildMember.id
		self.name = guildMember.display_name
		self.points = 0
		self.active = True
	
	#Returns a list used in quiz standings.
	async def getStandingsRow(self, rank):
		return [
			TableCell(
				"{rank}.".format(rank = rank)
				,"<"
			)
			,TableCell(
				"{player.name}".format(player = self)
				,"<"
			)
			,TableCell(
				"{player.points:.2f}".format(player = self)
				,">"
			)
		]