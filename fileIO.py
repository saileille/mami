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
	text = await getCsvVar(messageCode, "general", "languages\\" + language)
	return text

async def getLanguageCode(language, messageText):
	variable = await getCsvVar(messageText, "general", "languages\\" + language, invert=1)
	return variable

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
	
	#We are presuming the structure contains several objects.
	if (type(jsonObject) is list):
		objects = await convertToObjectList(jsonObject)
	else:
		#Must otherwise be a dictionary.
		objects = await convertToObjectDict(jsonObject)
	
	return objects

async def savePickle(data, filename, folder=""):
	filepath = await getFilePath(filename + ".db", folder)
	
	with open(filepath, mode="wb") as file:
		pickle.dump(data, file)

async def deleteFile(filename, folder=""):
	filepath = await getFilePath(filename, folder)
	os.remove(filepath)

		