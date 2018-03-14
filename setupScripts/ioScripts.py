import copy
import json
import pickle

pickle.DEFAULT_PROTOCOL = 4

def getFilePath(filename, folder=""):
	with open("filepath.txt", mode="r") as file:
		filepath = file.read()
		filepath += "\\"
	
	if (folder != ""):
		return filepath + folder + "\\" + filename
	
	return filepath + filename

def saveCommandsPickle(commands):
	#fileList = getFilePath("commandList.db", "staticData")
	fileDict = getFilePath("commands.db", "staticData")
	
	commandDict = copy.deepcopy(commands)
	convSubCommands(commandDict)
	"""
	with open(fileList, mode="wb") as file:
		pickle.dump(commands, file)
	"""
	with open(fileDict, mode="wb") as file:
		pickle.dump(commandDict, file)
	
	saveCommandNameTemplate(commandDict)

def convSubCommands(command):
	commandDict = {}
	
	for subCommand in command.sub_commands:
		if (len(subCommand.sub_commands) > 0):
			convSubCommands(subCommand)
		
		commandDict[subCommand.name] = subCommand
	
	command.sub_commands = commandDict

def saveCommandsJson(commands):
	template = getFilePath("cmdTemplate.json", "languages")
	
	with open(template, mode="w", encoding="utf-8") as file:
		json.dump(commands, file, ensure_ascii=False, indent="\t")

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

def saveCommandNameTemplate(commands):
	filepath = getFilePath("commandNames.json", "languages")
	
	commands = commands.__dict__
	simpleCommands = {}
	
	simpleCommands["sub_commands"] = getSimpleSubCommands(commands["sub_commands"])
	
	saveCommandsJson(simpleCommands)

def getSimpleSubCommands(command):
	simpleCommands = {}
	
	for key in command:
		sub_command = command[key].__dict__
		
		simpleCommands[key] = {}
		simpleCommands[key]["name"] = ""
		
		simpleCommands[key]["sub_commands"] = getSimpleSubCommands(sub_command["sub_commands"])
	
	return simpleCommands

def convToDict(dict):
	#Converts objects inside dict to dict.
	newDict = {}
	
	for key in dict:
		newDict[key] = dict[key].__dict__
		newDict[key]["sub_commands"] = convToDict(newDict[key]["sub_commands"])
	
	return newDict