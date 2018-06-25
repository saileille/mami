import asyncio
import math
import random

from bot import client
from fileIO import getLanguageText
from rpgFunctions import getPlayerObject, getUserObject, saveUserObject
from sendFunctions import processMsg, sendToUser

#Contains all information about the specific round.
class RPGBattleRound(object):
	def __init__(
		self
		,belligerents = {}
	):
		self.belligerents = belligerents
	
	async def actionPhaseCompleted(self):
		for id in self.belligerents:
			if (self.belligerents[id].action == None):
				return False
		
		return True
	
	async def dealDamage(self, id, thisUser, opponentId, opponentUser):
		actions = self.belligerents[id].actions
		thisAction = self.belligerents[id].action
		damageType = await self.compareActions(id, opponentId)
		
		damageLevel = 0
		if (actions[thisAction].type == "offence"):
			damageLevel = thisUser.rpg_character.offence
		elif (actions[thisAction].type == "defence"):
			damageLevel = thisUser.rpg_character.defence
		
		damageLevel *= -1
		
		if (damageType == "fullDamage"):
			self.belligerents[opponentId].hp_change = damageLevel
		elif (damageType == "speedCheck"):
			speedModifier = await self.getSpeedModifier(thisUser.rpg_character, opponentUser.rpg_character)
			
			self.belligerents[opponentId].hp_change = math.floor(damageLevel * speedModifier)
		
		opponentUser.rpg_character.hp += self.belligerents[opponentId].hp_change
		await saveUserObject(opponentUser)
	
	async def compareActions(self, id, opponentId):
		actions = self.belligerents[id].actions
		thisAction = self.belligerents[id].action
		opponentAction = self.belligerents[opponentId].action
		
		return actions[thisAction].effects[opponentAction]
	
	async def processActions(self):
		battleContinues = True
		
		characterObjects = {}
		for id in self.belligerents:
			opponentId = await self.getOpponentId(id)
			user = await getUserObject(id)
			opponentUser = await getUserObject(opponentId)
			
			await self.dealDamage(id, user, opponentId, opponentUser)
			
			if (id not in characterObjects):
				characterObjects[id] = user
				characterObjects[id] = opponentUser
		
		for id in self.belligerents:
			user = characterObjects[id]
			if (user.rpg_character.hp == 0):
				battleContinues = False
		
		return battleContinues
	
	async def getOpponentId(self, id):
		for opponentId in self.belligerents:
			if (id != opponentId):
				return opponentId
	
	async def getSpeedModifier(self, thisCharacter, opponentCharacter):
		speedModifier = 1 - 1.0 * opponentCharacter.speed / thisCharacter.speed
		
		if (speedModifier < 0):
			return 0
		
		return speedModifier
	
	#Information about the round's events.
	async def getEvents(self, language):
		actions = []
		hpChanges = []
		
		for id in self.belligerents:
			actions.append(
				await self.belligerents[id].getActionString(language)
			)
			hpChange = await self.belligerents[id].getHpChangeString(language)
			
			if (hpChange != None):
				hpChanges.append(
					hpChange
				)
		
		text = "\n".join(actions)
		
		if (len(hpChanges) != 0):
			text += "\n\n" + "\n".join(hpChanges)
		
		return text
	
	async def getOutcomes(self, language):
		codes = {}
		for id in self.belligerents:
			opponentId = await self.getOpponentId(id)
			player = await getPlayerObject(id)
			
			if (player.hp == 0):
				codes[id] = "RPG.CHARACTER_DIED"
				codes[opponentId] = "RPG.VICTORIOUS_BATTLE"
			elif (self.belligerents[opponentId].escaped == True):
				codes[id] = "RPG.OPPONENT_ESCAPED"
				codes[opponentId] = "RPG.ESCAPED_SAFELY"
		
		for id in codes:
			codes[id] = await processMsg(
				codes[id]
				,language
			)
		
		return codes