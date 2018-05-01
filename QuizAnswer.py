class QuizAnswer(object):
	def __init__(self, answer, rank, time):
		self.answer = answer
		
		#The position of the answer: first answer gets the number 1, second 2, etc.
		self.rank = rank
		
		#Time difference between question and answer.
		self.time = time