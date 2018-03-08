import json
import pickle
import copy

pickle.DEFAULT_PROTOCOL = 4

def getFilePath(filename, folder=""):
	if (folder != ""):
		return folder + "\\" + filepath
	
	return filename

def saveCommandsPickle(commands):
	fileList = getFilePath("commandList.db")
	fileDict = getFilePath("commandDict.db")
	
	commandDict = {}
	
	commands2 = copy.deepcopy(commands)
	
	for command in commands2:
		convSubCommands(command)
		commandDict[command.name] = command
	
	with open(fileList, mode="wb") as file:
		pickle.dump(commands, file)
	
	with open(fileDict, mode="wb") as file:
		pickle.dump(commandDict, file)

def convSubCommands(command):
	commandDict = {}
	
	for subCommand in command.sub_commands:
		if (len(subCommand.sub_commands) > 0):
			convSubCommands(subCommand)
		
		commandDict[subCommand.name] = subCommand
	
	command.sub_commands = commandDict

def saveCommandsJson(commands):
	listFile = getFilePath("commandList.json")
	dictFile = getFilePath("commandDict.json")
	testListFile = getFilePath("commandListTest.json")
	testDictFile = getFilePath("commandDictTest.json")
	
	commandDict = getCommandDict(commands)
	commandList = getCommandList(commandDict)
	
	with open(testListFile, mode="w", encoding="utf-8") as file:
		json.dump(commandList, file, ensure_ascii=False, indent="\t")
	
	with open(testDictFile, mode="w", encoding="utf-8") as file:
		json.dump(commandDict, file, ensure_ascii=False, indent="\t")
	
	with open(listFile, mode="w", encoding="utf-8") as file:
		json.dump(commandList, file, ensure_ascii=False, separators=(",", ":"))
	
	with open(dictFile, mode="w", encoding="utf-8") as file:
		json.dump(commandDict, file, ensure_ascii=False, separators=(",", ":"))

def getCommandDict(commands):
	commandDict = {}
	
	for key in commands:
		commands[key].code = key
		commandDict[key] = commands[key].__dict__
		commandDict[key]["CLASSNAME"] = "Command"
	
	return commandDict

def getCommandList(commandDict):
	commandList = []
	for key in commandDict:
		commandList.append(commandDict[key])
	
	return commandList


	