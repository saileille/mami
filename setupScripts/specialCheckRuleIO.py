from ioScripts import savePickle

from specialCheckRules import specialCheckRules

def saveSpecialCheckRules():
	savePickle(specialCheckRules, "specialCheckRules", "staticData")