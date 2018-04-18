from StringHandler import StringHandler

from bot import client
from fileIO import getLanguageText

#Has all sorts of dictionary-conversion functions.
class DictHandler(object):
	def __init__(
		self
		,dict = None
	):
		self.dict = dict
	
	#Returns a nice text thing. (Well said!)
	async def getPermissionInfoText(self, discordMessage, language):
		msgList = []
		
		for key in self.dict:
			msgList.append(
				await StringHandler(key).getLocalisedCommandString(language)
			)
			
			if ("server" in self.dict[key]):
				permissionObject = self.dict[key]["server"]
				
				msgList.append(
					await getLanguageText(language, "SERVER")
				)
				
				msgList += await permissionObject.getPermissionString(discordMessage, language)
			
			if ("channels" in self.dict[key]):
				msgList.append(
					await getLanguageText(language, "OVERRIDDEN_CHANNELS")
				)
				
				for channelKey in self.dict[key]["channels"]:
					#Get the channel object.
					channelObject = client.get_channel(channelKey)
					msgList.append(channelObject.name)
					
					permissionObject = self.dict[key]["channels"][channelKey]
					msgList += await permissionObject.getPermissionString(discordMessage, language)
		
		if (len(msgList) == 0):
			msgList.append(
				await getLanguageText(language, "INFO.PERMISSIONS.NO_PERMISSIONS_ON_SERVER")
			)
		
		return "\n\n".join(msgList)