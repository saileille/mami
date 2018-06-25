import json
import pickle

pickle.DEFAULT_PROTOCOL = 4

with open("filepath.txt", mode="r", encoding="utf-8") as file:
	root = file.read()
	root += "\\"

def getFilePath(filename, folder=""):
	if (folder != ""):
		return root + folder + "\\" + filename
	
	return root + filename

def readTextFile(filename, folder=""):
	filepath = getFilePath(filename + ".txt", folder)
	
	with open(filepath, encoding="utf-8", mode="r") as file:
		text = file.read()
	
	return text

def saveJson(data, filename, folder=""):
	filepath = getFilePath(filename + ".json", folder)
	
	jsonString = json.dumps(
		data
		,ensure_ascii = False
		,indent = "\t"
		,sort_keys = True
	)
	
	with open(filepath, "w", encoding="utf-8") as file:
		file.write(jsonString)

def loadJson(filename, folder=""):
	filepath = getFilePath(filename + ".json", folder)
	
	with open(filepath, mode="r", encoding="utf-8") as file:
		jsonObject = json.load(file)
	
	return jsonObject

def saveData(commands):
	saveCommandsPickle(commands)
	saveMakaLaugh()

def savePickle(data, filename, folder=""):
	filename = "{filename}.db".format(filename=filename)
	filepath = getFilePath(filename, folder)
	
	with open(filepath, mode="wb") as file:
		pickle.dump(data, file)