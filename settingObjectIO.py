#Save and load functions for setting objects.

import os

from Channel import Channel
from Server import Server
from User import User

from fileIO import deleteFile, loadPickle, savePickle

#Saves Server, Channel or User object.
#syncedServers is a list of servers yet to be synced, saveObject is what is to be saved.
#id is also the filename.
async def saveSettingObject(saveObject, id, syncList=None):
	#Making sure the ID is an integer.
	id = int(id)
	
	className = type(saveObject).__name__
	folder = "savedData\\{type}s".format(type=className.lower())
	
	if (await saveObject.isValid(id) == True):
		if (await saveObject.isDefault() == False):
			await savePickle(saveObject, id, folder)
		else:
			await deleteFile(
				"{id}.db".format(id = id)
				,folder
			)
	
	#If this is the first iteration.
	if (syncList == None):
		syncList = await getSyncedSettings(id, folder)
	
	if (len(syncList) > 1):
		syncList.remove(id)
		nextId = syncList[0]
		await saveSettingObject(saveObject, nextId, syncList)

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

async def deleteRpgCharacters():
	for dirpath, dirnames, filenames in os.walk("savedData\\users"):
		for file in filenames:
			id = file.replace(".db", "")
			
			userObject = await loadUserSettings(id)
			userObject.rpg_character = None
			await saveSettingObject(userObject, id)
	
	battleFolder = "savedData\\rpg\\battles"
	for dirpath, dirnames, filenames in os.walk(battleFolder):
		battleNames = filenames
	
	for battle in battleNames:
		await deleteFile(battle, battleFolder)