from QuizQuestion import QuizQuestion

from randomOrder import randomOrderSync

class QuizMultipleQuestion(QuizQuestion):
	def __init__(self, questionDict):
		super().__init__(questionDict)
		
		#Randomises the answer order immediately.
		self.answer_options = randomOrderSync(
			self.answer_options
		)