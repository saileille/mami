import asyncio

from MessageList import MessageList
from MessageVariables import MessageVariables

from bot import client
from fileIO import getLanguageText

#Send function that should handle everything.
#TODO: Functionality for filePaths
async def send(channel, msg=None, language=None, varDict={}, filePaths=None):
	if (msg != None):
		msg = await processMsg(msg, language, varDict)
	
	#Get the messages to be sent as a list.
	messages = MessageList(msg, filePaths)
	await messages.getMessageList()
	
	sentMessages = await messages.sendMessages(channel)
	return sentMessages

async def processMsg(msg, language=None, varDict={}):
	if (language != None):
		msg = await getLanguageText(language, msg)
	
	msg = msg.format(**varDict)
	return msg

#Sends a DM to the user given.
async def sendToUser(id, text, language=None, varDict={}):
	await send(
		await getUserDMChannel(id)
		,text
		,language
		,varDict
	)

async def getUserDMChannel(id):
	user = client.get_user(id)
	if (user.dm_channel == None):
		await user.create_dm()
	
	return user.dm_channel

async def askForMsg(channel, msg, check):
	await send(channel, msg)
	response = await client.wait_for("message", check = check)
	return response.content.strip()

async def countdownForUsers(idList, content, timer):
	channels = []
	for id in idList:
		channels.append(
			await getUserDMChannel(id)
		)
	
	return await countdown(channels, content, timer)

#Use this to make a visible time limit for the user to input a command.
async def countdown(messages, timer):
	countdownMsgList = []
	for message in messages:
		countdownMsgList.append(
			await message.send(timer)
		)
	
	while (timer > 0):
		await asyncio.sleep(1)
		timer -= 1
		for i in range(len(countdownMsgList)):
			message = countdownMsgList[i]
			content = await messages[i].getContent(timer)
			await message.edit(content=content)
	
	return countdownMsgList