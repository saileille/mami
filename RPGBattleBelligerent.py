from RPGBattleAction import RPGBattleAction

from fileIO import getLanguageText
from sendFunctions import processMsg, sendToUser

#Belligerent data for each phase. Used in RPGBattleRound class.
class RPGBattleBelligerent(object):
	actions = {
		"light_attack": RPGBattleAction(
			"light_attack"
			,"offence"
			,{
				"light_attack": "speedCheck"
				,"heavy_attack": "speedCheck"
				,"lunge": "speedCheck"
				,"parry": "fullDamage"
				,"block": "ineffective"
				,"dodge": "speedCheck"
			}
		)
		,"heavy_attack": RPGBattleAction(
			"heavy_attack"
			,"offence"
			,{
				"light_attack": "speedCheck"
				,"heavy_attack": "speedCheck"
				,"lunge": "speedCheck"
				,"parry": "speedCheck"
				,"block": "fullDamage"
				,"dodge": "ineffective"
			}
		)
		,"lunge": RPGBattleAction(
			"lunge"
			,"offence"
			,{
				"light_attack": "speedCheck"
				,"heavy_attack": "speedCheck"
				,"lunge": "speedCheck"
				,"parry": "ineffective"
				,"block": "speedCheck"
				,"dodge": "fullDamage"
			}
		)
		,"parry": RPGBattleAction(
			"parry"
			,"defence"
			,{
				"light_attack": "ineffective"
				,"heavy_attack": "speedCheck"
				,"lunge": "fullDamage"
				,"parry": "ineffective"
				,"block": "ineffective"
				,"dodge": "ineffective"
			}
		)
		,"block": RPGBattleAction(
			"block"
			,"defence"
			,{
				"light_attack": "fullDamage"
				,"heavy_attack": "ineffective"
				,"lunge": "speedCheck"
				,"parry": "ineffective"
				,"block": "ineffective"
				,"dodge": "ineffective"
			}
		)
		,"dodge": RPGBattleAction(
			"dodge"
			,"defence"
			,{
				"light_attack": "speedCheck"
				,"heavy_attack": "fullDamage"
				,"lunge": "ineffective"
				,"parry": "ineffective"
				,"block": "ineffective"
				,"dodge": "ineffective"
			}
		)
	}
	
	def __init__(
		self
		,id
		,name
	):
		self.id = id
		self.name = name
		self.action = None
		self.hp_change = 0
		self.escaped = False
	
	async def getActionChoices(self):
		text = ""
		for actionName in self.actions:
			action = self.actions[actionName]
			
			if (text != ""):
				text += "\n"
			
			text += ">" + action.name + " (" + action.type + ")"
		
		return text
	
	async def getActionString(self, language):
		return await processMsg(
			"RPG.CHARACTER_ACTION"
			,language
			,{
				"name": self.name
				,"action": self.action
			}
		)
	
	async def getHpChangeString(self, language):
		text = None
		
		if (self.hp_change > 0):
			text = "RPG.POS_HP_CHANGE"
		elif (self.hp_change < 0):
			text = "RPG.NEG_HP_CHANGE"
		
		if (text != None):
			text = await processMsg(
				text
				,language
				,{
					"name": self.name
					,"hp": abs(self.hp_change)
				}
			)
		
		return text