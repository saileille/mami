import csv
import pickle
import json
import os

pickle.DEFAULT_PROTOCOL = 4

async def getFilePath(filename, folder=""):
	if (folder != ""):
		return folder + "\\" + filename
	
	return filename

def getFilePathSync(filename, folder=""):
	if (folder != ""):
		return folder + "\\" + filename
	
	return filename

async def getCsvVar(variable, filename, folder="", invert=0):
	#Gets a specific variable from a CSV file.
	#CSV is used for simple variables.
	#If invert = 1, returns the variable name from text.
	
	filepath = await getFilePath(filename + ".csv", folder)
	
	with open(filepath, encoding="utf-8", mode="r") as file:
		reader = csv.reader(file, dialect="excel", delimiter=";")
		for row in reader:
			if (row[0 + invert] == variable):
				return row[1 - invert]

def getCsvVarSync(variable, filename, folder="", invert=0):
	#Gets a specific variable from a CSV file.
	#CSV is used for simple variables.
	#If invert = 1, returns the variable name from text.
	
	filepath = getFilePathSync(filename + ".csv", folder)
	
	with open(filepath, encoding="utf-8", mode="r") as file:
		reader = csv.reader(file, dialect="excel", delimiter=";")
		for row in reader:
			if (row[0 + invert] == variable):
				return row[1 - invert]

async def getLanguageText(language, messageCode):
	defaultLanguage = await getCsvVar("DEFAULT_LANGUAGE", "basic", "staticData")
	defaultLanguage = "english"
	text = await getCsvVar(messageCode, "general", "languages\\" + language)
	
	if (text == None):
		text = await getCsvVar(messageCode, "general", "languages\\" + defaultLanguage)
	
	if (text == None):
		return messageCode
	
	return text

async def getLanguageCode(language, messageText):
	defaultLanguage = await getCsvVar("DEFAULT_LANGUAGE", "basic", "staticData")
	code = await getCsvVar(messageText, "general", "languages\\" + language, invert=1)
	
	if (code == None):
		#If not found, tries to find the code from the default language.
		code = await getCsvVar(messageText, "general", "languages\\" + defaultLanguage, invert=1)
	
	return code

async def getCommandCode(language, text, prevCodes=[]):
	#prevCodes is a list of codes found previously.
	#Used to direct the search to the right path.
	
	cmdDict = await loadJson("cmdNames", "languages\\" + language)
	
	for code in prevCodes:
		cmdDict = cmdDict["sub_commands"][code]
	
	for key in cmdDict["sub_commands"]:
		if (text == cmdDict["sub_commands"][key]["name"]):
			return key

async def getCommandName(language, code, prevCodes):
	#prevCodes is used to locate the proper command sub-directory.
	#code indicates the end of search and the name we want.
	
	cmdDict = await loadJson("cmdNames", "languages\\" + language)
	
	for prevCode in prevCodes:
		if (prevCode == None):
			break
		
		cmdDict = cmdDict["sub_commands"][prevCode]
	
	return cmdDict["sub_commands"][code]["name"]

async def loadPickle(filename, folder="", default=None):
	filepath = await getFilePath(filename + ".db", folder)
	
	#Exception handling is only done if the default object exists.
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

async def savePickle(data, filename, folder=""):
	filepath = await getFilePath(filename + ".db", folder)
	
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