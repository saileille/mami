import html

from QuizAnswer import QuizAnswer

from fileIO import getLanguageText

class QuizQuestion(object):
	def __init__(self, questionDict):
		self.category = questionDict["category"]
		self.difficulty = questionDict["difficulty"]
		self.question = questionDict["question"]
		self.correct_answer = questionDict["correct_answer"]
		self.answer_options = questionDict["incorrect_answers"] + [self.correct_answer]
		self.answers = {}
		self.order_number = 0
		self.time = 0
	
	#Because the questions come in an encoded state.
	async def decodeHtml(self):
		self.category = html.unescape(self.category)
		self.difficulty = html.unescape(self.difficulty)
		self.question = html.unescape(self.question)
		self.correct_answer = html.unescape(self.correct_answer)
		
		decodedAnswerOptions = []
		for option in self.answer_options:
			decodedAnswerOptions.append(
				html.unescape(option)
			)
		
		self.answer_options = decodedAnswerOptions
	
	#Gives a string to display to the players.
	async def getQuestionString(self):
		#print("Correct Answer: " + self.correct_answer)
		
		text = "*{category}\n{difficulty}*\n\n**{question}**\n".format(
			category = self.category
			,difficulty = self.difficulty
			,question = self.question
		)
		
		for i in range(len(self.answer_options)):
			option = self.answer_options[i]
			number = i + 1
			text += "\n**{number}**: {option}".format(
				number = number
				,option = option
			)
		
		return text
	
	#Gets the actual answer based on the number given, and places it in the answer list.
	#Returns whether the operation was successful or not.
	async def convertAnswer(self, message, id, answer):
		if (answer > 0 and answer <= len(self.answer_options)):
			self.answers[id] = QuizAnswer(
				self.answer_options[answer - 1]
				,len(self.answers) + 1
			)
			
			await self.answers[id].setTime(message, self.time)
			return True
		else:
			return False
	
	async def getCorrectAnswerString(self, language):
		return "{correctAnswer} **{answer}**".format(
			correctAnswer = await getLanguageText(language, "QUIZ.CORRECT_ANSWER")
			,answer = self.correct_answer
		)
	
	async def getTimestamp(self, msg):
		self.time = msg.created_at.timestamp()