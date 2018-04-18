#Functions that deal with synchronising server and channel settings.

from StringHandler import StringHandler

from bot import client
from bot import send
from fileIO import getLanguageText
from fileIO import loadSync
from fileIO import saveSync
from permissionFunctions import checkCommandPermission
from settingObjectIO import loadChannelSettings
from settingObjectIO import loadServerSettings

#Returns a boolean based on whether the target channel is in order.
#Current checks:
#If the channel exists.
#If the channel is in a server.
#If the user is in the targeted server.
#If the user has permissions to use sync command on the target channel.
async def checkChannelSyncTarget(message, channelId):
	channelObject = client.get_channel(channelId)
	
	#The server object can be accessed with channelObject.server.
	
	#If non-existing channel.
	if (channelObject == None):
		await send(
			message.discord_py.channel
			,await getLanguageText(
				message.language
				,"CHANNEL_NOT_FOUND"
			)
		)
		
		return False
	
	#If a non-server channel.
	if (type(channelObject).__name__ == "PrivateChannel"):
		await send(
			message.discord_py.channel
			,await getLanguageText(
				message.language
				,"PRIVATE_CHANNELS_NOT_ALLOWED"
			)
		)
		
		return False
	
	#Fetching settings of the target channel.
	channelSettings = await loadChannelSettings(channelId)
	serverSettings = await loadServerSettings(channelObject.guild.id)
	
	#Member object of the target server.
	userObject = channelObject.guild.get_member(message.discord_py.author.id)
	
	if (userObject == None):
		await send(
			message.discord_py.channel
			,await getLanguageText(
				message.language
				,"USER_NOT_ON_SYNC_SERVER"
			)
		)
		
		return False
	
	COMMAND_LIST = [
		"settings"
		,"channel"
		,"sync"
		,"add"
	]
	
	permissionGranted = await checkCommandPermission(
		userObject
		,serverSettings
		,channelSettings
		,COMMAND_LIST
		,channelObject
	)
	
	if (permissionGranted == False):
		await send(
			message.discord_py.channel
			,await getLanguageText(
				message.language
				,"NO_PERMISSION_TO_SYNC"
			)
		)
	
	return permissionGranted

#Adds synchronisation relationships.
async def synchroniseChannel(message, arguments):
	channelIds = [message.discord_py.channel.id]
	for channel in arguments:
		id = await StringHandler(channel).getId("channel")
		
		#TODO: Lots of checking here.
		
		if (await checkChannelSyncTarget(message, id) == False):
			return
		
		channelIds.append(id)
	
	await addSync(channelIds, "channels")
	
	channelsSynced = await getLanguageText(message.language, "CHANNELS_SYNCED")
	#channelsSynced.format(channels=channels)
	
	await send(message.discord_py.channel, channelsSynced)

async def addSync(idList, type):
	#type is either "channels", "servers" or "users"
	folder = "savedData\\" + type
	existingSyncs = await loadSync(type)
	
	for id in idList:
		for syncList in existingSyncs:
			if (id in syncList):
				await appendToExistingSync(idList, syncList)
				break
	else:
		existingSyncs.append(idList)
	
	await saveSync(existingSyncs, folder)

async def appendToExistingSync(idList, syncList):
	for id in idList:
		if (id not in syncList):
			syncList.append(id)

#Removes synchronisation relationships. Does not necessarily require arguments.
async def unsynchroniseChannel(message, arguments):
	channelIds = [message.discord_py.channel.id]
	for channel in arguments:
		id = await StringHandler(channel).getId("channel")
		channelIds.append(id)
	
	await removeSync(channelIds, "channels")
	
	await send(
		message.discord_py.channel
		,await getLanguageText(
			message.language
			,"CHANNEL_SYNCS_REMOVED"
		)
	)

async def removeSync(idList, type):
	#type is either "channels", "servers" or "users"
	folder = "savedData\\" + type
	existingSyncs = await loadSync(type)
	
	for id in idList:
		i = 0
		while (i < len(existingSyncs)):
			if (id in existingSyncs[i]):
				existingSyncs[i].remove(id)
				
				if (len(existingSyncs[i]) < 2):
					del existingSyncs[i]
					continue
			
			i += 1
	
	await saveSync(existingSyncs, folder)