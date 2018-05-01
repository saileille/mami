from QuizQuestion import QuizQuestion

class QuizBooleanQuestion(QuizQuestion):
	def __init__(self, questionDict):
		super().__init__(questionDict)
		
		self.answer_options.sort(reverse=True)