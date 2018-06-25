from ioScripts import readTextFile, saveJson

def saveMakaLaugh():
	laughDict = getLaughData()
	saveJson(laughDict, "makalaughs", "staticData")

def getLaughData():
	laughs = readTextFile("makalaughs", "setupScripts")
	laughList = laughs.split("\n")
	
	initials = getInitials(laughList)
	letters = getLetters(laughList)
	
	laughDict = {
		"initials": initials
		,"letters": letters
	}
	
	return laughDict

def getInitials(laughList):
	"""
	#example
	initials = {
		"A": 3
		,"H": 1
		,"U": 2
	}
	"""
	
	initials = {}
	for laugh in laughList:
		initial = laugh[0]
		if (initial in initials):
			initials[initial] += 1
		else:
			initials[initial] = 1
	
	return initials

def getLetters(laughList):
	"""
	#example
	letters = {
		"A": {
			"U": 4
			,"H: 12
		}
		,"H": {
			"A": 10
			,"U": 12
		}
		,"U": {
			"A": 3
			,"H": 10
		}
	}
	"""
	
	letters = {}
	for laugh in laughList:
		for i in range(len(laugh) - 1):
			letter = laugh[i]
			nextLetter = laugh[i + 1]
			
			if (letter not in letters):
				letters[letter] = {}
			
			if (nextLetter in letters[letter]):
				letters[letter][nextLetter] += 1
			else:
				letters[letter][nextLetter] = 1
	
	return letters

