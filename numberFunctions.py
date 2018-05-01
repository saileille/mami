#Miscellaneus number functions.

#Forces the number within the range given.
async def forceRange(number, min, max):
	if (number < min):
		return min
	elif (number > max):
		return max
	
	return number