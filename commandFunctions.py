from DictHandler import DictHandler
from MakaLaugh import MakaLaugh
from Permission import Permission
from PermissionChanger import PermissionChanger
from Prefix import Prefix
from QuizPlayer import QuizPlayer

from fileIO import getLanguageText, loadPickle
from lewdPictures import getLewds
from listFunctions import getVerbalList
from sendFunctions import send
from settingObjectIO import deleteRpgCharacters
from synchronisation import synchroniseChannel, unsynchroniseChannel, viewChannelSyncs

#Test command.
async def test(message, arguments):
	await send(
		message.discord_py.channel
		,"TEST.MESSAGE"
		,message.language
	)

#Shows the prefixes.
async def prefixView(message, arguments):
	prefix = Prefix(message)
	msg = await prefix.getPrefixStrings()
	
	await send(
		message.discord_py.channel
		,msg
	)

#Changes the server prefix.
async def prefixServerChange(message, arguments):
	await message.server_settings.changePrefix(message, arguments)

#Clears the server prefix.
async def prefixServerClear(message, arguments):
	await message.server_settings.clearPrefix(message)

#Changes the channel prefix.
async def prefixChannelChange(message, arguments):
	await message.channel_settings.changePrefix(message, arguments)

#Clears the channel prefix.
async def prefixChannelClear(message, arguments):
	await message.channel_settings.clearPrefix(message)

#Changes the user prefix.
async def prefixUserChange(message, arguments):
	await message.user_settings.changePrefix(message, arguments)

#Clears the user prefix.
async def prefixUserClear(message, arguments):
	await message.user_settings.clearPrefix(message)

async def settingsServerPermissionsGive(message, arguments):
	await message.server_settings.changePermissions(message, arguments, "allow")

async def settingsServerPermissionsDeny(message, arguments):
	await message.server_settings.changePermissions(message, arguments, "deny")

async def settingsServerPermissionsUndo(message, arguments):
	await message.server_settings.changePermissions(message, arguments, "undo")

async def settingsServerPermissionsClear(message, arguments):
	await message.server_settings.clearPermissions(message, arguments)

async def settingsChannelPermissionsGive(message, arguments):
	await message.channel_settings.changePermissions(message, arguments, "allow")

async def settingsChannelPermissionsDeny(message, arguments):
	await message.channel_settings.changePermissions(message, arguments, "deny")

async def settingsChannelPermissionsUndo(message, arguments):
	await message.channel_settings.changePermissions(message, arguments, "undo")

async def settingsChannelPermissionsClear(message, arguments):
	await message.channel_settings.clearPermissions(message, arguments)

#Shows command permissions for all commands on this server, and all channel-specific permissions.
async def infoPermissions(message, arguments):
	permissionDict = {}
	
	for channel in message.discord_py.guild.channels:
		try:
			channelSettings = await loadPickle(channel.id, "savedData\\channels")
			await channelSettings.getPermissionsPerCommand(permissionDict, channel.id)
		except FileNotFoundError:
			pass
	
	await message.server_settings.getPermissionsPerCommand(permissionDict)
	
	dictHandler = DictHandler(permissionDict)
	msgString = await dictHandler.getPermissionInfoText(message.discord_py, message.language)
	
	await send(
		message.discord_py.channel
		,msgString
	)

async def changeServerLanguage(message, arguments):
	await message.server_settings.changeLanguage(message, arguments)

async def changeChannelLanguage(message, arguments):
	await message.channel_settings.changeLanguage(message, arguments)

async def changeUserLanguage(message, arguments):
	await message.user_settings.changeLanguage(message, arguments)

async def clearServerLanguage(message, arguments):
	await message.server_settings.clearLanguage(message)

async def clearChannelLanguage(message, arguments):
	await message.channel_settings.clearLanguage(message)

async def clearUserLanguage(message, arguments):
	await message.user_settings.clearLanguage(message)

async def serverSync(message, arguments):
	return

async def channelSync(message, arguments):
	await synchroniseChannel(message, arguments)

async def channelUnsync(message, arguments):
	await unsynchroniseChannel(message, arguments)

async def channelSyncView(message, arguments):
	await viewChannelSyncs(message)

async def lewd(message, arguments):
	await getLewds(message, arguments, nsfw=False)

async def nsfwLewd(message, arguments):
	await getLewds(message, arguments, nsfw=True)

async def maka(message, arguments):
	if (len(arguments) == 0):
		maka = MakaLaugh()
	elif(len(arguments) == 1):
		maka = MakaLaugh(min=arguments[0], max=arguments[0])
	else:
		maka = MakaLaugh(min=arguments[0], max=arguments[1])
	
	await maka.sendLaugh(message)

async def newQuiz(message, arguments):
	await message.channel_settings.newQuiz(message, arguments[0])

async def joinQuiz(message, arguments):
	await message.channel_settings.quiz.joinPlayer(message)

async def startQuiz(message, arguments):
	await message.channel_settings.quiz.start(message)

async def answerQuiz(message, arguments):
	await message.channel_settings.quiz.answer(message, arguments[0])

async def endQuiz(message, arguments):
	msg = await message.channel_settings.endQuiz(message)
	
	await message.save()
	await send(
		message.discord_py.channel
		,msg
	)

async def showQuizQuestion(message, arguments):
	await message.channel_settings.quiz.showQuestion(message)

async def changeQuizPointDistribution(message, arguments):
	await message.channel_settings.quiz.changePointDistribution(message, arguments[0])

async def changeQuizPointMultiplier(message, arguments):
	await message.channel_settings.quiz.changePointMultiplier(message, arguments[0])

async def newRpgCharacter(message, arguments):
	await message.user_settings.newRpgCharacter(message)

async def rpgTestDuel(message, arguments):
	await message.user_settings.rpg_character.startTestDuel(message, " ".join(arguments))

async def delAllRpgCharacters(message, arguments):
	await deleteRpgCharacters()
	await send(
		message.discord_py.channel
		,"RPG.DELALL.DONE"
		,message.language
	)

async def rpgBattleChooseAction(message, arguments):
	await message.user_settings.rpg_character.chooseAction(message, arguments[0])

async def rpgChangeOffence(message, arguments):
	await message.user_settings.rpg_character.changeAttr(message, "offence", arguments[0])

async def rpgChangeDefence(message, arguments):
	await message.user_settings.rpg_character.changeAttr(message, "defence", arguments[0])

async def rpgChangeHardiness(message, arguments):
	await message.user_settings.rpg_character.changeAttr(message, "hardiness", arguments[0])

async def rpgChangeSpeed(message, arguments):
	await message.user_settings.rpg_character.changeAttr(message, "speed", arguments[0])

async def rpgChangeHp(message, arguments):
	await message.user_settings.rpg_character.changeAttr(message, "hp", arguments[0])

async def rpgShowCharacterInfo(message, arguments):
	await message.user_settings.rpg_character.showInfo(message)