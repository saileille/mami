#Functions that deal with synchronising server and channel settings.
from discord import TextChannel

from StringHandler import StringHandler

from bot import client
from sendFunctions import send
from fileIO import getLanguageText
from fileIO import loadSync
from fileIO import saveSync
from idFunctions import isPossibleId
from permissionFunctions import checkCommandPermission
from settingObjectIO import loadChannelSettings
from settingObjectIO import loadServerSettings

async def viewChannelSyncs(message):
	channelIds = []
	
	for channel in message.discord_py.guild.channels:
		channelIds.append(channel.id)
	
	channelSyncList = await getSyncChannelList(message, channelIds)
	
	varDict = {}
	msg = "NO_CHANNEL_SYNCS"
	if (channelSyncList != ""):
		msg = "ALL_CHANNEL_SYNCS"
		varDict["channel_synclist"] = channelSyncList
	
	await send(
		message.discord_py.channel
		,msg
		,message.language
		,varDict
	)

#Checks if the channel exists, and is a text channel on a server.
async def isValidChannel(message, channelId, channelObject):
	botName = message.discord_py.guild.me.display_name
	
	#If non-existing channel.
	if (channelObject == None):
		await send(
			message.discord_py.channel
			,"CHANNEL_NOT_FOUND"
			,message.language
			,{
				"id": channelId
				,"bot_name": botName
			}
		)
		return False
	
	#If not a text channel on server.
	if (isinstance(channelObject, TextChannel) == False):
		await send(
			message.discord_py.channel
			,"NOT_TEXT_CHANNEL_ON_SERVER"
			,message.language
			,{
				"id": channelId
			}
		)
		return False
	
	return True

#Returns a boolean based on whether the target channel is in order.
#Current checks:
#If the channel exists.
#If the channel is a text channel in a server.
#If the user is in the targeted server.
#If the user has permissions to use sync command on the target channel.
async def checkChannelSyncTarget(message, channelId):
	channelObject = client.get_channel(channelId)
	
	#The server object can be accessed with channelObject.guild.
	
	if (await isValidChannel(message, channelId, channelObject) == False):
		return False
	
	#Fetching settings of the target channel.
	channelSettings = await loadChannelSettings(channelId)
	serverSettings = await loadServerSettings(channelObject.guild.id)
	
	#Member object of the target server.
	userObject = channelObject.guild.get_member(message.discord_py.author.id)
	
	if (userObject == None):
		msg = await getLanguageText(message.language, "USER_NOT_ON_SYNC_SERVER")
		msg = msg.format(id=channelId)
		
		await send(
			message.discord_py.channel
			,"USER_NOT_ON_SYNC_SERVER"
			,message.language
			,{
				"id": channelId
			}
		)
		return False
	
	#The path of this command.
	COMMAND_LIST = [
		"settings"
		,"channel"
		,"sync"
		,"add"
	]
	
	#Checking permission for every sub-command in order, just like when sending a command message.
	for i in range(len(COMMAND_LIST)):
		permissionGranted = await checkCommandPermission(
			userObject
			,serverSettings
			,channelSettings
			,COMMAND_LIST[:i + 1]
			,channelObject
		)
		
		if (permissionGranted == False):
			await send(
				message.discord_py.channel
				,"NO_PERMISSION_TO_SYNC_CHANNEL"
				,message.language
				,{
					"name": channelObject.name
				}
			)
			break
	
	return permissionGranted

async def getSyncChannelString(id, message):
	channelObject = client.get_channel(id)
	
	if (channelObject != None):
		text = "#{name} ({id})".format(name=channelObject.name, id=id)
		
		if (channelObject.guild != message.discord_py.guild):
			text += " - {name}".format(name=channelObject.guild.name)
	else:
		text = "[{unknownChannel}] ({id})".format(
			unknownChannel = await getLanguageText(message.language, "UNKNOWN_CHANNEL")
			,id = id
		)
	
	return text

#Shows synchronisations for the listed IDs. No duplicate lists are shown.
#If ignoreId is given, the output ignores the channel of that particular ID.
async def getSyncChannelList(message, idList, ignoreId=None):
	text = ""
	
	syncs = await loadSync("channels")
	
	for syncList in syncs:
		for id in idList:
			if (id in syncList):
				text += "```"
				textAdded = False
				
				for i in range(len(syncList)):
					if (syncList[i] != ignoreId):
						if (textAdded == True):
							text += "\n"
						
						text += await getSyncChannelString(syncList[i], message)
						
						if (textAdded == False):
							textAdded = True
				
				text += "```"
			
			break
	
	return text

#Adds synchronisation relationships.
async def synchroniseChannel(message, arguments):
	channelIds = [message.discord_py.channel.id]
	for channel in arguments:
		id = await StringHandler(channel).getId("channel")
		
		if (id == None):
			await invalidChannelIdFormat(message, channel)
			return
		
		if (await checkChannelSyncTarget(message, id) == False):
			return
		
		channelIds.append(id)
	
	await addSync(channelIds, "channels")
	
	await send(
		message.discord_py.channel
		,"CHANNELS_SYNCED"
		,message.language
		,{
			"channel_synclist": await getSyncChannelList(
				message
				,channelIds
				,ignoreId = message.discord_py.channel.id
			)
		}
	)

async def invalidChannelIdFormat(message, id):
	#If the ID is valid but lacking type identification, Mami will suggest putting the letter at the front.
	msg = "INVALID_CHANNEL_ID_NON_NUMBER"
	if (isPossibleId(id) == True):
		msg = "INVALID_CHANNEL_ID_NUMBER"
	
	await send(
		message.discord_py.channel
		,msg
		,message.language
		,{
			"id": id
		}
	)

async def addSync(idList, type):
	#type is either "channels", "servers" or "users"
	folder = "savedData\\" + type
	syncs = await loadSync(type)
	
	#This boolean exists to find out if the IDs were already added to an existing sync list.
	foundExisting = False
	
	for syncList in syncs:
		for id in idList:
			if (id in syncList):
				await appendToExistingSync(idList, syncList)
				foundExisting = True
				break
		
		if (foundExisting == True):
			break
	else:
		syncs.append(idList)
	
	await saveSync(syncs, folder)

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
		,"CHANNEL_SYNCS_REMOVED"
		,message.language
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