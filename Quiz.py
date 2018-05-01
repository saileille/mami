from enum import Enum, auto

from QuizPlayer import QuizPlayer
from QuizBooleanQuestion import QuizBooleanQuestion
from QuizMultipleQuestion import QuizMultipleQuestion

from fileIO import getLanguageText, loadJsonFromWeb
from listFunctions import getVerbalList
from sendFunctions import send

#Class for just the quiz API for now...

#https://opentdb.com/api_category.php - Listing of categories

class Quiz(object):
	basic_quiz = "https://opentdb.com/api.php?amount={questionAmount}"
	
	#Change this to 2 when not testing.
	min_players = 1
	
	class PointDistribution(Enum):
		EQUAL = auto()
		ORDER = auto()
	
	def __init__(self, question_count, host):
		self.question_count = question_count
		self.host = host
		
		self.players = {}
		self.players[host.id] = host
		self.started = False
		self.questions = []
		self.point_distribution = self.PointDistribution.EQUAL
	
	async def joinPlayer(self, message):
		if (self.started == True):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.ALREADY_ONGOING")
			)
			return
		
		author = message.discord_py.author
		
		#Must not have joined already
		if (author.id in self.players):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.JOIN.ALREADY_JOINED")
			)
			return
		
		self.players[author.id] = QuizPlayer(author)
		await message.save()
		
		msg = await getLanguageText(message.language, "QUIZ.JOIN.COMPLETED")
		msg = msg.format(
			participants = await self.getParticipants()
		)
		
		await send(message.discord_py.channel, msg)
	
	async def start(self, message):
		if (message.discord_py.author.id not in self.players):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.NOT_PARTAKING")
			)
			return
		
		if (self.started == True):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.ALREADY_ONGOING")
			)
			return
		
		if (len(self.players) < self.min_players):
			msg = await getLanguageText(message.language, "QUIZ.START.NOT_ENOUGH_PLAYERS")
			msg = msg.format(minPlayers = self.min_players)
			
			await send(message.discord_py.channel, msg)
			return
		
		self.started = True
		await self.generateQuestions()
		
		await message.save()
		await send(
			message.discord_py.channel
			,await self.questions[0].getQuestionString()
		)
	
	async def answer(self, message, answer):
		author = message.discord_py.author
		
		if (author.id not in self.players):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.NOT_PARTAKING")
			)
			return
		
		if (self.started == False):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.NOT_STARTED")
			)
			return
		
		question = self.questions[0]
		player = self.players[author.id]
		
		if (author.id in question.answers):
			msg = await getLanguageText(message.language, "QUIZ.A.ALREADY_ANSWERED")
			msg = msg.format(player = player.name)
			
			await send(message.discord_py.channel, msg)
			return
		
		if (await question.convertAnswer(author.id, answer) == False):
			msg = await getLanguageText(message.language, "QUIZ.A.OUT_OF_RANGE")
			msg = msg.format(
				maxNumber = len(question.answer_options)
			)
			
			await send(message.discord_py.channel, msg)
			return
		
		msg = await self.getAnswerConfirmation(message.language, author)
		
		#If everyone has answered, next question is put forth.
		for id in self.players:
			if (
				self.players[id].active
				and id not in question.answers
			):
				break
		else:
			msg += "\n\n" + await self.nextQuestionProcedure(message)
		
		await message.save()
		await send(message.discord_py.channel, msg)
	
	async def showQuestion(self, message):
		if (self.started == False):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.NOT_STARTED")
			)
			return
		
		msg = await self.questions[0].getQuestionString()
		msg += "\n\n{unanswered}".format(
			unanswered = await self.getUnansweredPlayers(message.language)
		)
		
		await send(message.discord_py.channel, msg)
	
	async def changePointDistribution(self, message, newPointDistribution):
		if (self.started == True):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.ALREADY_ONGOING")
			)
			return
		
		for pointDistribution in self.PointDistribution:
			if (newPointDistribution == pointDistribution.name):
				self.point_distribution = pointDistribution
				break
		else:
			msg = await getLanguageText(message.language, "QUIZ.SETTINGS.PLAYMODE.INVALID")
			msg = msg.format(
				pointDistribution = newPointDistribution
			)
			
			await send(message.discord_py.channel, msg)
			return
		
		await message.save()
		await send(
			message.discord_py.channel
			,await getLanguageText(message.language, "QUIZ.SETTINGS.PLAYMODE.CHANGED")
		)
	
	#Called when moving on to a new question.
	async def nextQuestionProcedure(self, message):
		text = await self.showGivenPoints(message.language)
		text += "\n{standings}".format(
			standings = await self.getStandings(message.language)
		)
		del self.questions[0]
		
		if (len(self.questions) == 0):
			text += "\n{endQuiz}".format(
				endQuiz = await message.channel_settings.endQuiz(message)
			)
		else:
			text += "\n\n{question}".format(
				question = await self.questions[0].getQuestionString()
			)
		
		return text
	
	async def generateQuestions(self):
		url = self.basic_quiz.format(questionAmount = self.question_count)
		
		quizData = await loadJsonFromWeb(url)
		
		if (quizData["response_code"] != 0):
			#Something went wrong.
			return
		
		for question in quizData["results"]:
			if (question["type"] == "multiple"):
				questionObject = QuizMultipleQuestion(question)
			elif (question["type"] == "boolean"):
				questionObject = QuizBooleanQuestion(question)
			
			await questionObject.decodeHtml()
			self.questions.append(questionObject)
	
	#Rewards points based on correct answers. Less correct answers, more points per player.
	async def showGivenPoints(self, language):
		question = self.questions[0]
		text = "{correctAnswer}\n".format(
			correctAnswer = await question.getCorrectAnswerString(language)
		)
		
		correctPlayers = await self.givePoints()
		
		if (len(correctPlayers) == 0):
			text += await getLanguageText(language, "QUIZ.NO_POINTS_REWARD")
		else:
			text += await getLanguageText(language, "QUIZ.POINTS_REWARD")
			text = text.format(
				players = await self.getPointRewardString(correctPlayers)
			)
		
		return text
	
	async def getParticipants(self):
		participants = []
		for id in self.players:
			participants.append(self.players[id].name)
		
		participants.sort()
		return "\n" + "\n".join(participants)
	
	#Returns a text confirming that the player has answered the question.
	async def getAnswerConfirmation(self, language, author):
		text = await getLanguageText(language, "QUIZ.A.ANSWERED_COMPLETE")
		
		text = text.format(
			player = self.players[author.id].name
		)
		
		return text
	
	async def getUnansweredPlayers(self, language):
		unansweredPlayers = []
		for playerId in self.players:
			if (playerId not in self.questions[0].answers):
				unansweredPlayers.append(self.players[playerId].name)
		
		unansweredPlayers.sort()
		
		if (len(unansweredPlayers) == 0):
			return ""
		else:
			text = await getLanguageText(language, "QUIZ.UNANSWERED_PLAYERS")
			text += "```\n{unanswered}```".format(
				unanswered = "\n".join(unansweredPlayers)
			)
			return text
	
	async def getStandings(self, language):
		text = "{standings}```".format(
			standings = await getLanguageText(language, "QUIZ.STANDINGS")
		)
		playerList = await self.rankPlayers()
		
		for i in range(len(playerList)):
			player = playerList[i]
			prevPlayer = playerList[i - 1]
			
			if (
				i == 0
				or prevPlayer.points != player.points
			):
				rank = i + 1
			
			text += "\n{player}".format(
				player = await player.getStandingsString(rank)
			)
		
		return text + "```"
	
	#Returns players in a ranked player list.
	async def rankPlayers(self):
		playerList = []
		for id in self.players:
			playerList.append(self.players[id])
		
		playerList.sort(
			key = lambda player: player.name
		)
		playerList.sort(
			key = lambda player: player.points
			,reverse = True
		)
		
		return playerList
	
	#Returns the winner names. Returns None if no points have been given.
	async def getWinners(self):
		playerList = await self.rankPlayers()
		
		#If no points have been awarded yet.
		if (playerList[0].points == 0):
			return None
		
		winnerNames = []
		for i in range(len(playerList)):
			player = playerList[i]
			prevPlayer = playerList[i - 1]
			
			if (i == 0 or player.points == prevPlayer.points):
				winnerNames.append(player.name)
			else:
				break
		
		return winnerNames
	
	async def getEndString(self, language):
		winnerList = await self.getWinners()
		
		if (winnerList != None):
			if (len(winnerList) == 1):
				text = await getLanguageText(language, "QUIZ.END.WINNER")
			else:
				text = await getLanguageText(language, "QUIZ.END.WINNERS")
			
			winnerString = await getVerbalList(language, winnerList)
		else:
			winnerString = ""
			text = await getLanguageText(language, "QUIZ.END.NO_WINNER")
		
		return text.format(winners = winnerString)
	
	async def givePoints(self):
		question = self.questions[0]
		
		correctPlayers = []
		for id in question.answers:
			answer = question.answers[id]
			if (answer.answer == question.correct_answer):
				correctPlayers.append({
					"id": id
					,"name": self.players[id].name
					,"rank": answer.rank
				})
		
		if (len(correctPlayers) == 0):
			pointMultiplier = 0
		else:
			pointMultiplier = 1.0 * len(self.players) / len(correctPlayers)
		
		correctPlayers.sort(
			key = lambda player: player["rank"]
		)
		
		for i in range(len(correctPlayers)):
			playerDict = correctPlayers[i]
			id = playerDict["id"]
			
			playerDict["rank"] = i + 1
			playerDict["points"] = await self.getPoints(playerDict, pointMultiplier)
			self.players[id].points += playerDict["points"]
		
		correctPlayers.sort(
			key = lambda playerDict: playerDict["name"]
		)
		correctPlayers.sort(
			key = lambda playerDict: playerDict["points"]
			,reverse = True
		)
		
		return correctPlayers
	
	async def getPointRewardString(self, correctPlayers):
		text = "```"
		for player in correctPlayers:
			text += "\n{name} - {points:.2f}".format(
				name = player["name"]
				,points = player["points"]
			)
		
		return text + "```"
	
	async def getPoints(self, player, pointMultiplier):
		if (self.point_distribution.name == "EQUAL"):
			return pointMultiplier
		elif (self.point_distribution.name == "ORDER"):
			return pointMultiplier / player["rank"]
		else:
			print("Quiz mode not recognised")
			return 0