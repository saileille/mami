from SpecialCheckRule import *
from specialCheckFunctions import *

specialCheckRules = {
	"noQuiz": SpecialCheckRule(
		pre_check = noQuiz
		,description = "QUIZ.ALREADY_EXISTS"
	)
	,"quizExists": SpecialCheckRule(
		pre_check = quizExists
		,description = "QUIZ.DOES_NOT_EXIST"
	)
	,"notJoinedQuiz": SpecialCheckRule(
		pre_check = notJoinedQuiz
		,description = "QUIZ.JOIN.ALREADY_JOINED"
	)
	,"joinedQuiz": SpecialCheckRule(
		pre_check = joinedQuiz
		,description = "QUIZ.NOT_PARTAKING"
	)
	,"quizNotOngoing": SpecialCheckRule(
		pre_check = quizNotOngoing
		,description = "QUIZ.ALREADY_ONGOING"
	)
	,"quizOngoing": SpecialCheckRule(
		pre_check = quizOngoing
		,description = "QUIZ.NOT_STARTED"
	)
	,"quizEnoughPlayers": SpecialCheckRule(
		pre_check = quizEnoughPlayers
		,description = "QUIZ.START.NOT_ENOUGH_PLAYERS"
	)
	,"quizNotAnswered": SpecialCheckRule(
		pre_check = quizNotAnswered
		,description = "QUIZ.A.ALREADY_ANSWERED"
	)
	,"quizHost": SpecialCheckRule(
		post_check = quizHost
	)
	,"noRpgCharacter": SpecialCheckRule(
		pre_check = noRpgCharacter
		,description = "RPG.NEW.HAS_RPG_CHARACTER"
	)
	,"hasRpgCharacter": SpecialCheckRule(
		pre_check = hasRpgCharacter
		,description = "RPG.NO_RPG_CHARACTER"
	)
	,"rpgCharacterNotInBattle": SpecialCheckRule(
		pre_check = rpgCharacterNotInBattle
		,description = "RPG.CHARACTER_IN_BATTLE"
	)
	,"rpgCharacterInBattle": SpecialCheckRule(
		pre_check = rpgCharacterInBattle
		,description = "RPG.CHARACTER_NOT_IN_BATTLE"
	)
	,"rpgNoActionChosen": SpecialCheckRule(
		pre_check = rpgNoActionChosen
		,description = "RPG.ALREADY_CHOSEN_ACTION"
	)
}