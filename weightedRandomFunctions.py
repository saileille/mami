#Various weighted random-related functions.

import random

#Get random index from a list of integers.
async def weightedIntegerList(intList):
	totalCount = 0
	
	for number in intList:
		totalCount += number
	
	rand = random.randrange(totalCount)
	progress = 0
	for i in range(len(intList)):
		progress += intList[i]
		if (rand < progress):
			return i
	
	#Something went wrong.
	return -1