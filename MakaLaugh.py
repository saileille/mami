import random

from fileIO import getCsvVar
from numberFunctions import forceRange
from sendFunctions import send

#Because Maka deserves her own class.
#And she is classy.
class MakaLaugh(object):
	def __init__(self, min=None, max=None):
		self.min = min
		self.max = max
		self.length = -1
	
	async def adjustLength(self):
		CHARACTER_LIMIT = int(
			await getCsvVar("MAX_CHARACTERS", "basic", "staticData")
		)
		
		#If min = None, it means nothing has been given.
		if (self.min == None):
			self.length = random.randint(3, 200)
			return
		
		self.min = await forceRange(self.min, 3, CHARACTER_LIMIT)
		self.max = await forceRange(self.max, 3, CHARACTER_LIMIT)
		
		values = sorted([self.min, self.max])
		self.length = random.randint(values[0], values[1])
	
	async def getLaugh(self):
		letters = ["A", "E", "H", "U"]
		laughString = ""
		prevLetter = None
		
		while (len(laughString) < self.length):
			selectedLetter = random.choice(letters)
			laughString += selectedLetter
			
			if (prevLetter != None):
				letters.append(prevLetter)
			
			prevLetter = selectedLetter
			letters.remove(prevLetter)
		
		return laughString
	
	async def sendLaugh(self, message):
		await self.adjustLength()
		await send(message.discord_py.channel, await self.getLaugh())