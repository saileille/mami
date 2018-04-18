import copy
import json
import os
import pickle

pickle.DEFAULT_PROTOCOL = 4

with open("filepath.txt", mode="r", encoding="utf-8") as file:
	root = file.read()
	root += "\\"

def getFilePath(filename, folder=""):
	if (folder != ""):
		return root + folder + "\\" + filename
	
	return root + filename

def saveCommandsPickle(commands):
	fileDict = getFilePath("commands.db", "staticData")
	
	commandDict = copy.deepcopy(commands)
	convSubCommands(commandDict)
	"""
	with open(fileList, mode="wb") as file:
		pickle.dump(commands, file)
	"""
	with open(fileDict, mode="wb") as file:
		pickle.dump(commandDict, file)
	
	#Converts all objects to dictionaries in preparation for JSON'ing.
	jsonDict = commands.getDict()
	
	saveCommandNameTemplate(jsonDict)
	updateCommandNames(jsonDict)

def convSubCommands(command):
	commandDict = {}
	
	for subCommand in command.sub_commands:
		if (len(subCommand.sub_commands) > 0):
			convSubCommands(subCommand)
		
		commandDict[subCommand.name] = subCommand
	
	command.sub_commands = commandDict

def saveCommandNameTemplate(commands):
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

def convToDict(dict):
	#Converts objects inside dict to dict.
	newDict = {}
	
	for key in dict:
		newDict[key] = dict[key].__dict__
		newDict[key]["sub_commands"] = convToDict(newDict[key]["sub_commands"])
	
	return newDict

def updateCommandNames(commands):
	for language, dirnames, filenames in os.walk(root + "\\languages"):
		for file in filenames:
			if (file == "cmdNames.json"):
				path = language + "\\" + file
				with open(path, mode="r", encoding="utf-8") as file:
					jsonObject = json.load(file)
				
				updateSubCommands(commands, jsonObject)
				
				with open(path, mode="w", encoding="utf-8") as file:
					json.dump(jsonObject, file, ensure_ascii=False, indent="\t")

def updateSubCommands(commands, localisation):
	#Removing old ones.
	removeKeys = []
	for key in localisation["sub_commands"]:
		if (key not in commands["sub_commands"]):
			removeKeys.append(key)
	
	for key in removeKeys:
		del localisation["sub_commands"][key]
	
	#Adding new ones.
	for key in commands["sub_commands"]:
		command = commands["sub_commands"][key]
		
		if (key not in localisation["sub_commands"]):
			localisation["sub_commands"][key] = {
				"name": "COMMANDNAME_HERE"
				,"sub_commands": {}
			}
		
		updateSubCommands(command, localisation["sub_commands"][key])