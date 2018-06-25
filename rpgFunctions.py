from fileIO import deleteFile, loadPickle, savePickle

#Returns the player object of the ID.
async def getPlayerObject(id):
	folder = "savedData\\users"
	user = await loadPickle(id, folder)
	return user.rpg_character

async def getUserObject(id):
	folder = "savedData\\users"
	return await loadPickle(id, folder)

async def saveUserObject(user, id=0):
	if (id == 0):
		id = user.rpg_character.id
	
	folder = "savedData\\users"
	
	if (await user.isDefault() == False):
		await savePickle(user, id, folder)
	else:
		await deleteFile(
			"{id}.db".format(id = id)
			,folder
		)