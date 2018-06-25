class QuizAnswer(object):
	def __init__(self, answer, rank):
		self.answer = answer
		
		#The position of the answer: first answer gets the number 1, second 2, etc.
		self.rank = rank
		
		#Time difference between question and answer.
		self.time = 0
	
	async def setTime(self, message, questionTimestamp):
		timestamp = message.discord_py.created_at.timestamp()
		self.time = timestamp - questionTimestamp
		print(self.time)