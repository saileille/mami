class RPGBattleAction(object):
	def __init__(self, name, type, effects):
		self.name = name
		self.type = type
		
		#Determines how the action behaves in relation to other actions.
		self.effects = effects