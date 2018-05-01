import random

#My (in my opinion) better way of randomising a list than random.shuffle.
async def randomOrder(list):
	newList = []
	
	while (0 < len(list)):
		index = random.randrange(len(list))
		newList.append(
			list.pop(index)
		)
	
	return newList

def randomOrderSync(list):
	newList = []
	
	while (0 < len(list)):
		index = random.randrange(len(list))
		newList.append(
			list.pop(index)
		)
	
	return newList