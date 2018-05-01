from Command import *
from commandFunctions import *
import ioScripts

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
								"string"
							]
							,optional_arguments_type = "string"
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
								"string"
							]
							,optional_arguments_type = "string"
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
								"string"
							]
							,optional_arguments_type = "string"
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
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsServerPermissionsGive
								)
								,Command(
									name = "deny"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsServerPermissionsDeny
								)
								,Command(
									name = "undo"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsServerPermissionsUndo
								)
								,Command(
									name = "clear"
									,argument_types = [
										"string"
									]
									,optional_arguments_type = "string"
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
										"string"
									]
									,optional_arguments_type = "string"
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
								"string"
							]
							,optional_arguments_type = "string"
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
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsChannelPermissionsGive
								)
								,Command(
									name = "deny"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsChannelPermissionsDeny
								)
								,Command(
									name = "undo"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsChannelPermissionsUndo
								)
								,Command(
									name = "clear"
									,argument_types = [
										"string"
									]
									,optional_arguments_type = "string"
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
										"string"
									]
									,optional_arguments_type = "string"
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
										"string"
									]
									,optional_arguments_type = "string"
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
										"string"
									]
									,optional_arguments_type = "string"
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
			,optional_arguments_type = "int"
			,function = maka
		)
		,Command(
			name = "quiz"
			,sub_commands = [
				Command(
					name = "new"
					,argument_types = [
						"int"
					]
					,function = newQuiz
				)
				,Command(
					name = "join"
					,function = joinQuiz
				)
				,Command(
					name = "start"
					,function = startQuiz
				)
				,Command(
					name = "a"
					,delete_message = True
					,argument_types = [
						"int"
					]
					,function = answerQuiz
				)
				,Command(
					name = "end"
					,function = endQuiz
				)
				,Command(
					name = "q"
					,function = showQuizQuestion
				)
				,Command(
					name = "settings"
					,sub_commands = [
						Command(
							name = "point_distribution"
							,argument_types = [
								"string"
							]
							,function = changeQuizPointsDistribution
						)
					]
				)
			]
			,server_only = True
		)
	]
)

ioScripts.saveCommandsPickle(commands)

input("Success. Press any key to exit.")