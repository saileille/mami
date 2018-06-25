import random

from fileIO import getCsvVar, loadJson, readTextFile
from numberFunctions import forceRange
from sendFunctions import send
from weightedRandomFunctions import weightedIntegerList

#Because Maka deserves her own class.
#And she is classy.
class MakaLaugh(object):
	def __init__(self, min=None, max=None):
		self.min = min
		self.max = max
		self.length = -1
		self.laugh = None
	
	async def sendLaugh(self, message):
		await self.adjustLength()
		await self.getLaugh()
		
		await send(
			message.discord_py.channel
			,self.laugh
		)
	
	async def getLaugh(self):
		laughs = await loadJson("makalaughs", "staticData")
		self.laugh = await self.getLetter(laughs["initials"])
		
		while (len(self.laugh) < self.length):
			self.laugh += await self.getNextLetter(laughs["letters"])
	
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
	
	async def getLetter(self, letters):
		letterList = []
		weightList = []
		
		for letter in letters:
			letterList.append(letter)
			weightList.append(letters[letter])
		
		index = await weightedIntegerList(weightList)
		return letterList[index]
	
	async def getNextLetter(self, letters):
		prevLetter = self.laugh[-1]
		return await self.getLetter(letters[prevLetter])