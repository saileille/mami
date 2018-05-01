from Quiz import Quiz
from QuizPlayer import QuizPlayer
from Server import Server

from bot import client
from fileIO import getLanguageText
from listFunctions import getVerbalList
from sendFunctions import send

#Channel-specific configuration.

class Channel(Server):
	def __init__(
		self
		,language = None
		,prefix = None
		,shortcuts = {}
		,lists = {}
		,autoresponses = {}
		,permissions = {}
		,quiz = None
	):
		super().__init__(
			language
			,prefix
			,shortcuts
			,lists
			,autoresponses
			,permissions
		)
		self.quiz = quiz
	
	#Checks if the Channel object is the default one.
	async def isDefault(self, serverLanguage):
		await self.cleanPermissions()
		
		if (
			self.language != None
			and self.language != serverLanguage
		):
			return False
		
		if (self.prefix != None):
			return False
		
		if (len(self.shortcuts) > 0):
			return False
		
		if (len(self.lists) > 0):
			return False
		
		if (len(self.autoresponses) > 0):
			return False
		
		if (len(self.permissions) > 0):
			return False
		
		if (self.quiz != None):
			return False
		
		return True
	
	#Forces the object to its default values.
	async def forceDefault(self):
		self.language = None
		self.prefix = None
		self.shortcuts = {}
		self.lists = {}
		self.autoresponses = {}
		self.permissions = {}
		self.quiz = None
	
	#Returns a boolean indicating whether the channel exists.
	async def isValid(self, id):
		return bool(client.get_channel(id))
	
	#Assigns the permissions to the dictionary.
	#This function is slightly different for server.
	async def getPermissionsPerCommand(self, permissionDict, channelID):
		for key in self.permissions:
			if (key not in permissionDict):
				permissionDict[key] = {}
			
			if ("channels" not in permissionDict[key]):
				permissionDict[key]["channels"] = {}
			
			permissionDict[key]["channels"][channelID] = self.permissions[key]
	
	async def newQuiz(self, message, questionCount):
		#Cannot add a new quiz if there already is one.
		if (self.quiz != None):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.ALREADY_EXISTS")
			)
			return
		
		#Question amount must be between 1 and 50.
		if (questionCount < 1 or questionCount > 50):
			await send(
				message.discord_py.channel
				,await getLanguageText(message.language, "QUIZ.NEW.INVALID_QUESTION_COUNT")
			)
			return
		
		self.quiz = Quiz(
			questionCount
			,QuizPlayer(message.discord_py.author)
		)
		
		await message.save()
		await send(
			message.discord_py.channel
			,await getLanguageText(message.language, "QUIZ.NEW.COMPLETED")
		)
	
	async def endQuiz(self, message):
		text = await self.quiz.getEndString(message.language)
		self.quiz = None
		return text