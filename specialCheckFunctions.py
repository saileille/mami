async def noQuiz(message):
	return message.channel_settings.quiz == None

async def quizExists(message):
	return message.channel_settings.quiz != None

async def notJoinedQuiz(message):
	quiz = message.channel_settings.quiz
	author = message.discord_py.author
	
	return author.id not in quiz.players

async def joinedQuiz(message):
	quiz = message.channel_settings.quiz
	author = message.discord_py.author
	
	return author.id in quiz.players

async def quizNotOngoing(message):
	return message.channel_settings.quiz.started == False

async def quizOngoing(message):
	return message.channel_settings.quiz.started

async def quizEnoughPlayers(message):
	quiz = message.channel_settings.quiz
	return len(quiz.players) >= quiz.min_players

async def quizNotAnswered(message):
	author = message.discord_py.author
	question = message.channel_settings.quiz.questions[0]
	
	return author.id not in question.answers

async def quizHost(message):
	author = message.discord_py.author
	host = message.channel_settings.quiz.host
	
	return host.id == author.id

async def noRpgCharacter(message):
	return message.user_settings.rpg_character == None

async def hasRpgCharacter(message):
	return message.user_settings.rpg_character != None

async def rpgCharacterNotInBattle(message):
	return await message.user_settings.rpg_character.getBattle() == None

async def rpgCharacterInBattle(message):
	return await message.user_settings.rpg_character.getBattle() != None

async def rpgNoActionChosen(message):
	battle = await message.user_settings.rpg_character.getBattle()
	player = battle.latest_round.belligerents[message.discord_py.author.id]
	return player.action == None