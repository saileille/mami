from ArgumentRule import *
from Command import *

from commandFunctions import *

commands = Command(
	name = "head"
	,all_prefixes = True
	,sub_commands = [
		Command(
			name = "test"
			,function = test
		)
		,Command(
			name = "prefix"
			,all_prefixes = True
			,sub_commands = [
				Command(
					name = "view"
					,all_prefixes = True
					,function = prefixView
				)
				,Command(
					name = "server"
					,sub_commands = [
						Command(
							name = "change"
							,argument_types = [
								ArgumentRule()
							]
							,optional_arguments_type = ArgumentRule()
							,function = prefixServerChange
						)
						,Command(
							name = "clear"
							,function = prefixServerClear
						)
					]
				)
				,Command(
					name = "channel"
					,sub_commands = [
						Command(
							name = "change"
							,argument_types = [
								ArgumentRule()
							]
							,optional_arguments_type = ArgumentRule()
							,function = prefixChannelChange
						)
						,Command(
							name = "clear"
							,function = prefixChannelClear
						)
					]
				)
				,Command(
					name = "user"
					,sub_commands = [
						Command(
							name = "change"
							,argument_types = [
								ArgumentRule()
							]
							,optional_arguments_type = ArgumentRule()
							,function = prefixUserChange
						)
						,Command(
							name = "clear"
							,function = prefixUserClear
						)
					]
				)
			]
		)
		,Command(
			name = "settings"
			,sub_commands = [
				Command(
					name = "server"
					,server_only = True
					,default_permissions = [
						"manage_guild"
					]
					,sub_commands = [
						Command(
							name = "permissions"
							,sub_commands = [
								Command(
									name = "give"
									,argument_types = [
										ArgumentRule()
										,ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsServerPermissionsGive
								)
								,Command(
									name = "deny"
									,argument_types = [
										ArgumentRule()
										,ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsServerPermissionsDeny
								)
								,Command(
									name = "undo"
									,argument_types = [
										ArgumentRule()
										,ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsServerPermissionsUndo
								)
								,Command(
									name = "clear"
									,argument_types = [
										ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsServerPermissionsClear
								)
							]
						)
						,Command(
							name = "language"
							,sub_commands = [
								Command(
									name = "change"
									,argument_types = [
										ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = changeServerLanguage
								)
								,Command(
									name = "clear"
									,function = clearServerLanguage
								)
							]
						)
						,Command(
							name = "sync_with"
							,argument_types = [
								ArgumentRule()
							]
							,optional_arguments_type = ArgumentRule()
							,default_permissions = [
								"administrator"
							]
							,function = serverSync
						)
					]
				)
				,Command(
					name = "channel"
					,server_only = True
					,default_permissions = [
						"manage_guild"
					]
					,sub_commands = [
						Command(
							name = "permissions"
							,sub_commands = [
								Command(
									name = "give"
									,argument_types = [
										ArgumentRule()
										,ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsChannelPermissionsGive
								)
								,Command(
									name = "deny"
									,argument_types = [
										ArgumentRule()
										,ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsChannelPermissionsDeny
								)
								,Command(
									name = "undo"
									,argument_types = [
										ArgumentRule()
										,ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsChannelPermissionsUndo
								)
								,Command(
									name = "clear"
									,argument_types = [
										ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = settingsChannelPermissionsClear
								)
							]
						)
						,Command(
							name = "language"
							,sub_commands = [
								Command(
									name = "change"
									,argument_types = [
										ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = changeChannelLanguage
								)
								,Command(
									name = "clear"
									,function = clearChannelLanguage
								)
							]
						)
						,Command(
							name = "sync"
							,default_permissions = [
								"administrator"
							]
							,sub_commands = [
								Command(
									name = "add"
									,argument_types = [
										ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,default_permissions = [
										"administrator"
									]
									,function = channelSync
								)
								,Command(
									name = "del"
									,optional_arguments_type = "string"
									,default_permissions = [
										"administrator"
									]
									,function = channelUnsync
								)
								,Command(
									name = "view"
									,function = channelSyncView
								)
							]
						)
					]
				)
				,Command(
					name = "user"
					,sub_commands = [
						Command(
							name = "language"
							,sub_commands = [
								Command(
									name = "change"
									,argument_types = [
										ArgumentRule()
									]
									,optional_arguments_type = ArgumentRule()
									,function = changeUserLanguage
								)
								,Command(
									name = "clear"
									,function = clearUserLanguage
								)
							]
						)
					]
				)
			]
		)
		,Command(
			name = "info"
			,sub_commands = [
				Command(
					name = "permissions"
					,server_only = True
					,function = infoPermissions
				)
			]
		)
		,Command(
			name = "lewd"
			,function = lewd
			,nsfw_function = nsfwLewd
		)
		,Command(
			name = "maka"
			,optional_arguments_type = ArgumentRule(
				conversion = "int"
			)
			,function = maka
		)
		,Command(
			name = "quiz"
			,sub_commands = [
				Command(
					name = "new"
					,argument_types = [
						ArgumentRule(
							conversion = "int"
						)
					]
					,special_checks = [
						"noQuiz"
					]
					,function = newQuiz
				)
				,Command(
					name = "join"
					,special_checks = [
						"quizExists"
						,"quizNotOngoing"
						,"notJoinedQuiz"
					]
					,function = joinQuiz
				)
				,Command(
					name = "start"
					,default_permissions = [
						"administrator"
					]
					,special_checks = [
						"quizExists"
						,"joinedQuiz"
						,"quizNotOngoing"
						,"quizEnoughPlayers"
						,"quizHost"
					]
					,function = startQuiz
				)
				,Command(
					name = "a"
					,delete_message = True
					,argument_types = [
						ArgumentRule(
							conversion = "int"
						)
					]
					,special_checks = [
						"quizExists"
						,"quizOngoing"
						,"joinedQuiz"
						,"quizNotAnswered"
					]
					,function = answerQuiz
				)
				,Command(
					name = "end"
					,default_permissions = [
						"administrator"
					]
					,special_checks = [
						"quizExists"
						,"quizHost"
					]
					,function = endQuiz
				)
				,Command(
					name = "q"
					,special_checks = [
						"quizExists"
						,"quizOngoing"
					]
					,function = showQuizQuestion
				)
				,Command(
					name = "settings"
					,sub_commands = [
						Command(
							name = "point_distribution"
							,argument_types = [
								ArgumentRule()
							]
							,default_permissions = [
								"administrator"
							]
							,special_checks = [
								"quizExists"
								,"quizNotOngoing"
								,"joinedQuiz"
								,"quizHost"
							]
							,function = changeQuizPointDistribution
						)
						,Command(
							name = "point_multiplier"
							,argument_types = [
								ArgumentRule()
							]
							,default_permissions = [
								"administrator"
							]
							,special_checks = [
								"quizExists"
								,"quizNotOngoing"
								,"joinedQuiz"
								,"quizHost"
							]
							,function = changeQuizPointMultiplier
						)
					]
					,default_permissions = [
						"administrator"
					]
					,special_checks = [
						"quizExists"
						,"quizNotOngoing"
						,"joinedQuiz"
						,"quizHost"
					]
				)
			]
			,server_only = True
		)
		,Command(
			name = "rpg"
			,sub_commands = [
				Command(
					name = "new"
					,special_checks = [
						"noRpgCharacter"
					]
					,function = newRpgCharacter
				)
				,Command(
					#Combat mechanic test function.
					name = "duel"
					,argument_types = [
						ArgumentRule()
					]
					,optional_arguments_type = ArgumentRule()
					,special_checks = [
						"hasRpgCharacter"
						,"rpgCharacterNotInBattle"
					]
					,function = rpgTestDuel
				)
				,Command(
					#Debugging function for deleting all characters.
					name = "delall"
					,owner_only = True
					,function = delAllRpgCharacters
				)
				,Command(
					name = "action"
					,argument_types = [
						ArgumentRule()
					]
					,special_checks = [
						"hasRpgCharacter"
						,"rpgCharacterInBattle"
						,"rpgNoActionChosen"
					]
					,function = rpgBattleChooseAction
				)
				,Command(
					name = "cheats"
					,sub_commands = [
						Command(
							name = "offence"
							,argument_types = [
								ArgumentRule(conversion="int")
							]
							,special_checks = [
								"hasRpgCharacter"
							]
							,function = rpgChangeOffence
						)
						,Command(
							name = "defence"
							,argument_types = [
								ArgumentRule(conversion="int")
							]
							,special_checks = [
								"hasRpgCharacter"
							]
							,function = rpgChangeDefence
						)
						,Command(
							name = "hardiness"
							,argument_types = [
								ArgumentRule(conversion="int")
							]
							,special_checks = [
								"hasRpgCharacter"
							]
							,function = rpgChangeHardiness
						)
						,Command(
							name = "speed"
							,argument_types = [
								ArgumentRule(conversion="int")
							]
							,special_checks = [
								"hasRpgCharacter"
							]
							,function = rpgChangeSpeed
						)
						,Command(
							name = "hp"
							,argument_types = [
								ArgumentRule(conversion="int")
							]
							,special_checks = [
								"hasRpgCharacter"
							]
							,function = rpgChangeHp
						)
					]
				)
				,Command(
					name = "character"
					,special_checks = [
						"hasRpgCharacter"
					]
					,function = rpgShowCharacterInfo
				)
			]
		)
	]
)