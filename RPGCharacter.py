import os

from RPGBattle import RPGBattle

from fileIO import deleteFile, getLanguageText, loadPickle, savePickle
from listFunctions import convToIntList
from rpgFunctions import getUserObject, saveUserObject
from sendFunctions import processMsg, send, sendToUser

#A character in the RPG, player-controlled or not.
class RPGCharacter(object):
	#The directory where the battles are kept
	battlesFolder = "savedData\\rpg\\battles"
	
	def __init__(
		self
		,id = 0
	):
		self.id = id
		self.name = None
		self.level = 1
		self.offence = 1
		self.defence = 1
		self.hardiness = 1
		self.speed = 1
		self.hp = 1
	
	@property
	def max_hp(self):
		return self.hardiness * 5
	
	@property
	def hp(self):
		return self.__hp
	
	@hp.setter
	def hp(self, hp):
		if (hp < 0):
			self.__hp = 0
		elif (hp > self.max_hp):
			self.__hp = self.max_hp
		else:
			self.__hp = hp
	
	#Returns the character's battle object, if one exists. Otherwise returns None.
	async def getBattle(self):
		battleName = await self.getBattleName()
		
		if (battleName == None):
			return None
		
		return await loadPickle(battleName, self.battlesFolder)
	
	#Gives just the battle name, not the object.
	async def getBattleName(self):
		for dirpath, dirnames, filenames in os.walk(self.battlesFolder):
			for file in filenames:
				#Getting the character IDs from the file.
				battleName = file.replace(".db", "")
				belligerents = await convToIntList(battleName.split("v"))
				
				if (self.id in belligerents):
					return battleName
		
		return None
	
	#Simple test-duelling function.
	async def startTestDuel(self, message, name):
		folder = "savedData\\users"
		
		for dirpath, dirnames, filenames in os.walk(folder):
			for file in filenames:
				filename = file.replace(".db", "")
				user = await loadPickle(filename, folder)
				
				opponent = user.rpg_character
				if (opponent != None and name == opponent.name):
					await self.createBattle(opponent, message.language)
					return
	
	#Creates a new battle file.
	async def createBattle(self, opponent, language):
		ids = [
			self.id
			,opponent.id
		]
		
		battle = RPGBattle(
			belligerents = ids
		)
		
		await battle.newRound(language)
		
		await savePickle(
			battle
			,await battle.getFileName()
			,"savedData\\rpg\\battles"
		)
	
	async def chooseAction(self, message, action):
		battleName = await self.getBattleName()
		battle = await loadPickle(battleName, self.battlesFolder)
		
		#This check can be removed once argument checks are done properly
		if (action not in battle.latest_round.belligerents[self.id].actions):
			await send(
				message.discord_py.channel
				,"RPG.ACTION.INVALID"
				,message.language
				,{
					"action": action
				}
			)
			return
		
		battle.latest_round.belligerents[self.id].action = action
		
		#Round should end here.
		if (await battle.latest_round.actionPhaseCompleted()):
			if (await battle.latest_round.processActions()):
				#Battle continues.
				await battle.newRound(message.language)
			else:
				#Battle ended.
				events = await battle.latest_round.getEvents(message.language)
				outcomes = await battle.latest_round.getOutcomes(message.language)
				
				for id in battle.belligerents:
					await sendToUser(
						id
						,events + "\n\n" + outcomes[id]
					)
				
				await deleteFile(battleName + ".db", self.battlesFolder)
				return
		
		else:
			await send(
				message.discord_py.channel
				,"RPG.ACTION_CHOSEN"
				,message.language
			)
		
		await savePickle(battle, battleName, self.battlesFolder)
	
	#Returns the HP string of the character used in battle.
	async def getHpString(self, language):
		return await processMsg(
			"RPG.HP_TEXT"
			,language
			,{
				"current": self.hp
				,"maximum": self.max_hp
			}
		)
	
	async def changeAttr(self, message, attribute, amount):
		setattr(self, attribute, amount)
		await message.save()
		
		await send(
			message.discord_py.channel
			,"{attribute} set to {amount}".format(
				attribute = attribute
				,amount = amount
			)
		)
	
	async def showInfo(self, message):
		vars = {"char": self}
		
		textList = [
			await processMsg(
				"RPG.CHARACTER.NAME"
				,message.language
				,vars
			)
			,await processMsg(
				"RPG.CHARACTER.OFFENCE"
				,message.language
				,vars
			)
			,await processMsg(
				"RPG.CHARACTER.DEFENCE"
				,message.language
				,vars
			)
			,await processMsg(
				"RPG.CHARACTER.HARDINESS"
				,message.language
				,vars
			)
			,await processMsg(
				"RPG.CHARACTER.SPEED"
				,message.language
				,vars
			)
			,await processMsg(
				"RPG.CHARACTER.HP"
				,message.language
				,vars
			)
		]
		
		await send(
			message.discord_py.channel
			,"\n".join(textList)
		)