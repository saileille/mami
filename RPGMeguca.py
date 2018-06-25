from RPGCharacter import RPGCharacter

#A magical girl in the RPG. Always player-controlled.
class RPGMeguca(RPGCharacter):
	def __init__(
		self
		,id = 0
	):
		super().__init__(
			id
		)
		self.weapon = None