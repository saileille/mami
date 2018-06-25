from RPGMeguca import RPGMeguca
from SettingObject import SettingObject

from bot import client
from fileIO import getLanguageText
from sendFunctions import askForMsg, processMsg, send

class User(SettingObject):
	def __init__(
		self
		,language = None
		,prefix = None
		,rpg_character = None
	):
		super().__init__(
			language
			,prefix
		)
		self.rpg_character = rpg_character
	
	#Checks if the User object is the default one.
	async def isDefault(self):
		if (self.language != None):
			return False
		
		if (self.prefix != None):
			return False
		
		if (self.rpg_character != None):
			return False
		
		return True
	
	async def forceDefault(self):
		self.language = None
		self.prefix = None
		self.rpg_character = None
	
	#Returns a boolean indicating whether the user can be reached by Mami.
	#Does not actually use the User class at all. Should be moved elsewhere.
	async def isValid(self, id):
		return bool(client.get_user(id))
	
	async def newRpgCharacter(self, message):
		def nameCheck(checkMsg):
			return (
				checkMsg.content != ""
				and checkMsg.author == message.discord_py.author
				and checkMsg.channel == message.discord_py.channel
			)
		
		def numberCheck(checkMsg):
			try:
				number = int(checkMsg.content)
				
				return (
					number > 0
					and checkMsg.author == message.discord_py.author
					and checkMsg.channel == message.discord_py.channel
				)
			except ValueError:
				return False
		
		self.rpg_character = RPGMeguca(
			id = message.discord_py.author.id
		)
		
		name = await askForMsg(
			message.discord_py.channel
			,await processMsg(
				"RPG.NEW.GIVE_NAME"
				,message.language
			)
			,nameCheck
		)
		self.rpg_character.name = name.replace("\n", " ")
		
		offence = await askForMsg(
			message.discord_py.channel
			,"How much offence?"
			,numberCheck
		)
		self.rpg_character.offence = int(offence)
		
		defence = await askForMsg(
			message.discord_py.channel
			,"How much defence?"
			,numberCheck
		)
		self.rpg_character.defence = int(defence)
		
		hardiness = await askForMsg(
			message.discord_py.channel
			,"How much hardiness?"
			,numberCheck
		)
		self.rpg_character.hardiness = int(hardiness)
		self.rpg_character.hp = self.rpg_character.max_hp
		
		speed = await askForMsg(
			message.discord_py.channel
			,"How much speed?"
			,numberCheck
		)
		self.rpg_character.speed = int(speed)
		
		await message.save()
		await send(
			message.discord_py.channel
			,"RPG.NEW.CHARACTER_CREATED"
			,message.language
		)