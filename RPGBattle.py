from CountdownMessage import CountdownMessage
from RPGBattleBelligerent import RPGBattleBelligerent
from RPGBattleRound import RPGBattleRound
from Table import Table
from TableCell import TableCell

from bot import client
from fileIO import getLanguageText
from listFunctions import convToStringList
from rpgFunctions import getPlayerObject
from sendFunctions import countdown, getUserDMChannel, processMsg, sendToUser

#Holds information about battles.
class RPGBattle(object):
	def __init__(
		self
		,belligerents = []
	):
		self.belligerents = belligerents
		self.rounds = []
	
	@property
	def latest_round(self):
		if (len(self.rounds) == 0):
			return None
		
		return self.rounds[-1]
	
	async def getFileName(self):
		self.belligerents.sort()
		return "v".join(await convToStringList(self.belligerents))
	
	async def generateNewRound(self):
		roundBelligerents = {}
		for id in self.belligerents:
			character = await getPlayerObject(id)
			
			roundBelligerents[id] = RPGBattleBelligerent(
				id = id
				,name = character.name
			)
		
		self.rounds.append(
			RPGBattleRound(belligerents = roundBelligerents)
		)
	
	async def newRound(self, language):
		topText = ""
		if (len(self.rounds) != 0):
			topText = await self.latest_round.getEvents(language)
		
		countdownText = await processMsg(
			"RPG.BATTLE_ROUND_ACTION"
			,language
		)
		
		await self.generateNewRound()
		
		messages = []
		for id in self.belligerents:
			await sendToUser(
				id
				,"{topText}{battleScreen}{countdownText}".format(
					topText = topText
					,battleScreen = await self.getBattleScreen(id, language)
					,countdownText = countdownText
				)
			)
	
	async def getOpponentId(self, id):
		if (self.belligerents[0] == id):
			return self.belligerents[1]
		
		return self.belligerents[0]
	
	async def getBattleScreen(self, id, language):
		#id means the player to whom the screen is displayed.
		opponentId = await self.getOpponentId(id)
		
		player = await getPlayerObject(id)
		opponent = await getPlayerObject(opponentId)
		
		table = Table()
		
		await table.addRow([
			TableCell(player.name, alignment="^")
			,TableCell(opponent.name, alignment="^", padding=5)
		])
		
		await table.addRow([
			TableCell(await player.getHpString(language), alignment="^")
			,TableCell(await opponent.getHpString(language), alignment="^", padding=5)
		])
		
		return "```\n{table}\n\n{actions}```".format(
			table = await table.getTableString()
			,actions = await self.latest_round.belligerents[id].getActionChoices()
		)