from enum import Enum, auto

from QuizPlayer import QuizPlayer
from QuizBooleanQuestion import QuizBooleanQuestion
from QuizMultipleQuestion import QuizMultipleQuestion
from Table import Table
from TableCell import TableCell

from fileIO import getLanguageText, loadJsonFromWeb
from listFunctions import getVerbalList
from sendFunctions import processMsg, send

#Class for just the quiz API for now...

#https://opentdb.com/api_category.php - Listing of categories

class Quiz(object):
	basic_quiz = "https://opentdb.com/api.php?amount={questionAmount}"
	
	#Change this to 2 when not testing.
	min_players = 1
	
	class PointDistribution(Enum):
		EQUAL = auto()
		ORDER = auto()
		TIME = auto()
	
	class PointMultiplier(Enum):
		FLAT = auto()
		WEIGHTED = auto()
	
	def __init__(self, question_count, host):
		self.question_count = question_count
		self.host = host
		
		self.players = {}
		self.players[host.id] = host
		self.started = False
		self.questions = []
		self.point_distribution = self.PointDistribution.EQUAL
		self.point_multiplier = self.PointMultiplier.WEIGHTED
	
	async def joinPlayer(self, message):
		author = message.discord_py.author
		
		self.players[author.id] = QuizPlayer(author)
		await message.save()
		
		await send(
			message.discord_py.channel
			,"QUIZ.JOIN.COMPLETED"
			,message.language
			,{
				"participants": await self.getParticipants()
			}
		)
	
	async def start(self, message):
		self.started = True
		await self.generateQuestions()
		
		questionMessages = await send(
			message.discord_py.channel
			,await self.questions[0].getQuestionString()
		)
		
		await self.questions[0].getTimestamp(questionMessages[0])
		await message.save()
	
	async def answer(self, message, answer):
		author = message.discord_py.author
		question = self.questions[0]
		player = self.players[author.id]
		
		if (author.id in question.answers):
			await send(
				message.discord_py.channel
				,"QUIZ.A.ALREADY_ANSWERED"
				,message.language
				,{
					"player": player.name
				}
			)
			return
		
		if (await question.convertAnswer(message, author.id, answer) == False):
			await send(
				message.discord_py.channel
				,"QUIZ.A.OUT_OF_RANGE"
				,message.language
				,{
					"max_number": len(question.answer_options)
				}
			)
			return
		
		msg = processMsg(
			"QUIZ.A.ANSWERED_COMPLETE"
			,message.language
			,{
				"player": self.players[author.id].name
			}
		)
		
		#If everyone has answered, next question is put forth.
		everyoneAnswered = False
		for id in self.players:
			if (
				self.players[id].active
				and id not in question.answers
			):
				break
		else:
			everyoneAnswered = True
			msg += "\n\n" + await self.nextQuestionProcedure(message)
		
		questionMessages = await send(
			message.discord_py.channel
			,msg
		)
		
		if (everyoneAnswered and len(self.questions) > 0):
			await self.questions[0].getTimestamp(questionMessages[0])
		
		await message.save()
	
	async def showQuestion(self, message):
		msg = await self.questions[0].getQuestionString()
		msg += "\n\n{unanswered}"
		
		await send(
			message.discord_py.channel
			,await self.questions[0].getQuestionString()
			,varDict = {
				"unanswered": await self.getUnansweredPlayers(message.language)
			}
		)
	
	async def changePointDistribution(self, message, newPointDistribution):
		for pointDistribution in self.PointDistribution:
			if (newPointDistribution == pointDistribution.name):
				self.point_distribution = pointDistribution
				break
		else:
			await send(
				message.discord_py.channel
				,"QUIZ.SETTINGS.POINT_DISTRIBUTION.INVALID"
				,message.language
				,{
					"point_distribution": newPointDistribution
				}
			)
			return
		
		await message.save()
		await send(
			message.discord_py.channel
			,"QUIZ.SETTINGS.POINT_DISTRIBUTION.CHANGED"
			,message.language
		)
	
	async def changePointMultiplier(self, message, newPointMultiplier):
		for pointMultiplier in self.PointMultiplier:
			if (newPointMultiplier == pointMultiplier.name):
				self.point_multiplier = pointMultiplier
				break
		else:
			msg = await getLanguageText(message.language, "QUIZ.SETTINGS.POINT_MULTIPLIER.INVALID")
			msg = msg.format(pointMultiplier = newPointMultiplier)
			
			await send(
				message.discord_py.channel
				,"QUIZ.SETTINGS.POINT_MULTIPLIER.INVALID"
				,message.language
				,{
					"point_multiplier": newPointMultiplier
				}
			)
			return
		
		await message.save()
		await send(
			message.discord_py.channel
			,"QUIZ.SETTINGS.POINT_MULTIPLIER.CHANGED"
			,message.language
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
		
		for i in range(len(quizData["results"])):
			question = quizData["results"][i]
			
			if (question["type"] == "multiple"):
				questionObject = QuizMultipleQuestion(question)
			elif (question["type"] == "boolean"):
				questionObject = QuizBooleanQuestion(question)
			
			questionObject.order_number = i + 1
			await questionObject.decodeHtml()
			
			self.questions.append(questionObject)
	
	#Rewards points based on correct answers. Less correct answers, more points per player.
	async def showGivenPoints(self, language):
		question = self.questions[0]
		text = "{correctAnswer}\n".format(
			correctAnswer = await question.getCorrectAnswerString(language)
		)
		
		correctPlayers = await self.givePoints()
		
		code = "QUIZ.NO_POINTS_REWARD"
		varDict = {}
		
		if (len(correctPlayers) > 0):
			code = "QUIZ.POINTS_REWARD"
			varDict["players"] = await self.getPointRewardString(correctPlayers)
		
		text += await processMsg(
			code
			,language
			,varDict
		)
		
		return text
	
	async def getParticipants(self):
		participants = []
		for id in self.players:
			participants.append(self.players[id].name)
		
		participants.sort()
		return "\n" + "\n".join(participants)
	
	async def getUnansweredPlayers(self, language):
		unansweredPlayers = []
		for playerId in self.players:
			if (playerId not in self.questions[0].answers):
				unansweredPlayers.append(
					"<@{id}>".format(id = playerId)
				)
		
		if (len(unansweredPlayers) == 0):
			return ""
		else:
			text = await getLanguageText(language, "QUIZ.UNANSWERED_PLAYERS")
			text += "\n{unanswered}".format(
				unanswered = "\n".join(unansweredPlayers)
			)
			return text
	
	async def getStandings(self, language):
		text = "{standings}```\n".format(
			standings = await processMsg(
				"QUIZ.STANDINGS"
				,language
			)
		)
		playerList = await self.rankPlayers()
		
		standings = Table()
		for i in range(len(playerList)):
			player = playerList[i]
			prevPlayer = playerList[i - 1]
			
			if (
				i == 0
				or prevPlayer.points != player.points
			):
				rank = i + 1
			
			await standings.addRow(
				await player.getStandingsRow(rank)
			)
		
		text += await standings.getTableString()
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
		
		varDict = {}
		code = "QUIZ.END.WINNER"
		
		if (winnerList != None):
			if (len(winnerList) > 1):
				code = "QUIZ.END.WINNERS"
			
			varDict["winners"] = await getVerbalList(language, winnerList)
		else:
			code = "QUIZ.END.NO_WINNER"
		
		return await processMsg(
			code
			,language
			,varDict
		)
	
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
					,"time": answer.time
				})
		
		pointMultiplier = await self.getPointMultiplier(correctPlayers)
		
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
		text = "```\n"
		
		correctList = Table()
		for player in correctPlayers:
			await correctList.addRow([
				TableCell(
					"{name}".format(name = player["name"])
					,"<"
				)
				,TableCell(
					"{points:.2f}".format(points = player["points"])
					,">"
				)
			])
		
		text += await correctList.getTableString()
		return text + "```"
	
	async def getPoints(self, player, pointMultiplier):
		if (self.point_distribution.name == "EQUAL"):
			return pointMultiplier
		
		elif (self.point_distribution.name == "ORDER"):
			return pointMultiplier / player["rank"]
		
		elif (self.point_distribution.name == "TIME"):
			if (player["time"] == 0):
				player["time"] == 0.000000000000001
			
			basePoints = 100 / player["time"]
			return pointMultiplier * basePoints
		
		else:
			print("Quiz mode not recognised")
			return 0
	
	async def getPointMultiplier(self, correctPlayers):
		if (len(correctPlayers) == 0):
			return 0
		
		if (self.point_multiplier.name == "WEIGHTED"):
			return 1.0 * len(self.players) / len(correctPlayers)
		
		elif (self.point_multiplier.name == "FLAT"):
			return 1.0