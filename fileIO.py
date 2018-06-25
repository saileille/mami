import csv
import json
import os
import pickle
import urllib.request

pickle.DEFAULT_PROTOCOL = 4

async def getFilePath(filename, folder=""):
	if (folder != ""):
		return folder + "\\" + filename
	
	return filename

def getFilePathSync(filename, folder=""):
	if (folder != ""):
		return folder + "\\" + filename
	
	return filename

async def readTextFile(filename, folder=""):
	filepath = await getFilePath(filename + ".txt", folder)
	
	with open(filepath, encoding="utf-8", mode="r") as file:
		text = file.read()
	
	return text

async def getCsvVar(variable, filename, folder="", invert=0, startsWith=""):
	#Gets a specific variable from a CSV file.
	#CSV is used for simple variables.
	#If invert = 1, returns the variable name from text.
	
	filepath = await getFilePath(filename + ".csv", folder)
	
	with open(filepath, encoding="utf-8", mode="r") as file:
		reader = csv.reader(file, dialect="excel", delimiter=";")
		for row in reader:
			#Checking the length so that empty rows can be allowed.
			#Checking the first character of the first row in case of comment.
			if (
				len(row) == 2
				and row[0][0] != "#"
			):
				returnRow = row[1 - invert]
				if (
					row[0 + invert] == variable
					and returnRow.startswith(startsWith)
				):
					return row[1 - invert]

def getCsvVarSync(variable, filename, folder="", invert=0):
	#Gets a specific variable from a CSV file.
	#CSV is used for simple variables.
	#If invert = 1, returns the variable name from text.
	
	filepath = getFilePathSync(filename + ".csv", folder)
	
	with open(filepath, encoding="utf-8", mode="r") as file:
		reader = csv.reader(file, dialect="excel", delimiter=";")
		for row in reader:
			#Checking the length so that empty rows can be allowed.
			#Checking the first character of the first row in case of comment.
			if (
				len(row) == 2
				and row[0][0] != "#"
			):
				if (row[0 + invert] == variable):
					return row[1 - invert]

async def getLanguageText(language, messageCode):
	defaultLanguage = await getDefaultLanguage()
	text = await getCsvVar(messageCode, "general", "languages\\" + language)
	
	if (text == None):
		return messageCode
	
	text = text.replace("\\n", "\n")
	return text

#Finds the CSV code. No longer needed.
async def getLanguageCode(language, messageText, startsWith=""):
	code = await getCsvVar(
		messageText
		,"general"
		,"languages\\" + language
		,invert = 1
		,startsWith = startsWith
	)
	
	#If not found, tries to find the code from the default language.
	if (code == None):
		defaultLanguage = await getDefaultLanguage()
		code = await getCsvVar(
			messageText
			,"general"
			,"languages\\" + defaultLanguage
			,invert = 1
			,startsWith = startsWith
		)
	
	return code

#Gets the global command code as a list.
async def getCommandCodeList(language, cmdNameList):
	cmdDict = await loadJson("cmdNames", "languages\\" + language)
	codeList = []
	
	for name in cmdNameList:
		for key in cmdDict["sub_commands"]:
			subCmd = cmdDict["sub_commands"][key]
			if (subCmd["name"] == name):
				cmdDict = cmdDict["sub_commands"][key]
				codeList.append(key)
				break
	
	return codeList

#prevCodes is used to locate the proper command sub-directory.
#code indicates the end of search and the name we want.
async def getCommandName(language, code, prevCodes):
	
	cmdDict = await loadJson("cmdNames", "languages\\" + language)
	
	for prevCode in prevCodes:
		if (prevCode == None):
			break
		
		cmdDict = cmdDict["sub_commands"][prevCode]
	
	return cmdDict["sub_commands"][code]["name"]

async def loadPickle(filename, folder = "", default = None):
	filename = "{filename}.db".format(filename=filename)
	filepath = await getFilePath(filename, folder)
	
	#Exception handling is only done if the default object has been explicitly given.
	if (default != None):
		try:
			with open(filepath, mode="rb") as file:
				data = pickle.load(file)
		except FileNotFoundError:
			return default
	else:
		with open(filepath, mode="rb") as file:
			data = pickle.load(file)
	
	return data

async def loadJson(filename, folder=""):
	filepath = await getFilePath(filename + ".json", folder)
	
	with open(filepath, mode="r", encoding="utf-8") as file:
		jsonObject = json.load(file)
	
	return jsonObject

async def loadJsonFromWeb(urlAddress):
	with urllib.request.urlopen(urlAddress) as url:
		jsonObject = json.loads(url.read().decode())
	
	return jsonObject

async def savePickle(data, filename, folder=""):
	filename = "{filename}.db".format(filename=filename)
	filepath = await getFilePath(filename, folder)
	
	with open(filepath, mode="wb") as file:
		pickle.dump(data, file)

async def deleteFile(filename, folder=""):
	filepath = await getFilePath(filename, folder)
	
	try:
		os.remove(filepath)
	except FileNotFoundError:
		pass

async def getPermissions():
	filepath = await getFilePath("permissions.txt", "staticData")
	
	with open(filepath, mode="r", encoding="utf-8") as file:
		permissionText = file.read()
	
	permissionList = permissionText.split("\n")
	return permissionList

def getBotToken():
	filepath = getFilePathSync("token.txt", "staticData")
	
	with open(filepath, mode="r", encoding="utf-8") as file:
		token = file.read()
	
	return token

async def loadCommands():
	commands = await loadPickle("commands", "staticData")
	return commands

async def getDefaultLanguage():
	defaultLanguage = await getCsvVar("DEFAULT_LANGUAGE", "basic", "staticData")
	return defaultLanguage

async def getDefaultPrefix():
	return await getCsvVar("DEFAULT_PREFIX", "basic", "staticData")

async def getCharacterLimit():
	return int(await getCsvVar("MAX_CHARACTERS", "basic", "staticData"))

#Returns a list of folders in the languages folder, i.e. all available languages.
async def getExistingLanguages(language):
	languages = []
	for folder in os.listdir("languages"):
		if (os.path.isdir(os.path.join("languages", folder))):
			languages.append(
				await getLanguageText(
					language
					,folder
				)
			)
	
	return languages

async def saveSync(existingSyncs, folder):
	if (len(existingSyncs) > 0):
		await savePickle(existingSyncs, "syncdata", folder)
	else:
		await deleteFile("syncdata.db", folder)

async def loadSync(type):
	folder = "savedData\\" + type
	syncs = await loadPickle("syncdata", folder, default=[])
	
	print(syncs)
	return syncs

async def getLewdList():
	folder = "staticData\\lewds"
	pictureNames = []
	
	for dirpath, dirnames, filenames in os.walk(folder):
		for file in filenames:
			pictureNames.append(await getFilePath(file, folder))
	
	return pictureNames

async def loadSpecialCheckRules():
	return await loadPickle("specialCheckRules", "staticData")