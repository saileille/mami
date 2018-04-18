#Save and load functions for setting objects.

from Channel import Channel
from Server import Server
from User import User

from fileIO import deleteFile
from fileIO import loadPickle
from fileIO import savePickle

#Saves Server, Channel or User object.
async def saveSettingObject(saveObject, id, language=None, syncList=None):
	#syncedServers is a list of servers yet to be synced, saveObject is what is to be saved.
	#id is also the filename.
	
	className = type(saveObject).__name__
	folder = "savedData\\{type}s".format(type=className.lower())
	
	#This structure is necessary because Channel's default check needs language.
	if (className != "Channel"):
		isDefault = await saveObject.isDefault()
	else:
		isDefault = await saveObject.isDefault(language)
	
	if (isDefault == False):
		await savePickle(saveObject, id, folder)
	else:
		idString = "{id}.db".format(id=id)
		await deleteFile(idString, folder)
	
	#If this is the first iteration.
	if (syncList == None):
		syncList = await getSyncedSettings(id, folder)
	
	if (len(syncList) > 1):
		syncList.remove(id)
		nextId = syncList[0]
		await saveSettingObject(saveObject, nextId, language, syncList)

#Loads Server, Channel or User object.

#Loads a Server object.
async def loadServerSettings(id):
	folder = "savedData\\servers"
	
	try:
		return await loadPickle(id, folder)
	except FileNotFoundError:
		defaultSettings = Server()
		await defaultSettings.forceDefault()
		return defaultSettings

#Loads a Channel object.
async def loadChannelSettings(id):
	folder = "savedData\\channels"
	
	try:
		return await loadPickle(id, folder)
	except FileNotFoundError:
		defaultSettings = Channel()
		await defaultSettings.forceDefault()
		return defaultSettings

#Loads a User object.
async def loadUserSettings(id):
	folder = "savedData\\users"
	
	try:
		return await loadPickle(id, folder)
	except FileNotFoundError:
		defaultSettings = User()
		await defaultSettings.forceDefault()
		return defaultSettings

async def getSyncedSettings(id, folder):
	existingSyncs = await loadPickle("syncdata", folder, default=[])
	
	for sync in existingSyncs:
		if (id in sync):
			return sync
	
	return []