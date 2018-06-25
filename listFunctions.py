from fileIO import getLanguageText

#All sorts of list functions here.
#Probably should convert StringHandler and DictHandler to something like this.

#Gives a nice little verbal list of a... list.
async def getVerbalList(language, stringList):
	text = ""
	for i in range(len(stringList)):
		if (i != 0):
			if (i < len(stringList) - 1):
				text += ", "
			else:
				text += " {wordAnd} ".format(
					wordAnd = await getLanguageText(language, "WORD_AND")
				)
		
		text += stringList[i]
	
	return text

async def convToStringList(list):
	newList = []
	
	for item in list:
		newList.append(
			str(item)
		)
	
	return newList

async def convToIntList(list):
	newList = []
	
	for item in list:
		newList.append(
			int(item)
		)
	
	return newList