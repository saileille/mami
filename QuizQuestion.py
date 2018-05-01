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
		
		text = "*{category}".format(category=self.category)
		text += "\n{difficulty}*".format(difficulty=self.difficulty)
		text += "\n\n**{question}**".format(question=self.question)
		
		text += "\n"
		
		for i in range(len(self.answer_options)):
			option = self.answer_options[i]
			number = i + 1
			
			text += "\n**{number}**: {option}".format(number=number, option=option)
		
		return text
	
	#Gets the actual answer based on the number given, and places it in the answer list.
	#Returns whether the operation was successful or not.
	async def convertAnswer(self, id, answer):
		if (answer > 0 and answer <= len(self.answer_options)):
			self.answers[id] = QuizAnswer(
				self.answer_options[answer - 1]
				,len(self.answers) + 1
				,None
			)
			
			return True
		else:
			return False
	
	async def getCorrectAnswerString(self, language):
		return "{correctAnswer} **{answer}**".format(
			correctAnswer = await getLanguageText(language, "QUIZ.CORRECT_ANSWER")
			,answer = self.correct_answer
		)
	
	async def getPoints(self, player, rewardMultiplier, quizMode):
		if (quizMode.name == "STANDARD"):
			return rewardMultiplier
		elif (quizMode.name == "ORDER"):
			return rewardMultiplier / player[rank]
		else:
			print("Quiz mode not recognised")
			return 0