#All sorts of things related to handling IDs.

#Returns a boolean revealing if the string is an ID without the identifying letter at the front.
async def isPossibleId(id):
	if (len(id) == 18):
		try:
			int(id)
			return True
		except ValueError:
			return False
	
	return False