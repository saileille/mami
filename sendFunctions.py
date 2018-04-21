from MessageList import MessageList

#Send function that should handle everything.
#TODO: Functionality for filePathList
async def send(channel, msg=None, filePaths=None):
	#Get the messages to be sent as a list.
	messages = MessageList(msg, filePaths)
	await messages.getMessageList()
	
	sentMessages = await messages.sendMessages(channel)
	
	return sentMessages