from Command import *
from commandFunctions import *
import ioScripts

commands = Command(
	name = "head"
	,all_prefixes = True
	,sub_commands = [
		Command(
			name = "test"
			,short_desc = "TEST.SHORTDESC"
			,function = test
		)
		,Command(
			name = "prefix"
			,short_desc = "PREFIX.SHORTDESC"
			,all_prefixes = True
			,sub_commands = [
				Command(
					name = "view"
					,short_desc = "PREFIX.VIEW.SHORTDESC"
					,all_prefixes = True
					,function = prefixView
				)
				,Command(
					name = "server"
					,short_desc = "PREFIX.SERVER.SHORTDESC"
					,sub_commands = [
						Command(
							name = "change"
							,short_desc = "PREFIX.SERVER.CHANGE.SHORTDESC"
							,long_desc = "prefix.server.change"
							,argument_help = "PREFIX.SERVER.CHANGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,optional_arguments_type = "string"
							,function = prefixServerChange
						)
						,Command(
							name = "clear"
							,short_desc = "PREFIX.SERVER.CLEAR.SHORTDESC"
							,function = prefixServerClear
						)
					]
				)
				,Command(
					name = "channel"
					,short_desc = "PREFIX.CHANNEL.SHORTDESC"
					,sub_commands = [
						Command(
							name = "change"
							,short_desc = "PREFIX.CHANNEL.CHANGE.SHORTDESC"
							,long_desc = "prefix.channel.change"
							,argument_help = "PREFIX.CHANNEL.CHANGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,optional_arguments_type = "string"
							,function = prefixChannelChange
						)
						,Command(
							name = "clear"
							,short_desc = "PREFIX.CHANNEL.CLEAR.SHORTDESC"
							,function = prefixChannelClear
						)
					]
				)
				,Command(
					name = "user"
					,short_desc = "PREFIX.USER.SHORTDESC"
					,sub_commands = [
						Command(
							name = "change"
							,short_desc = "PREFIX.USER.CHANGE.SHORTDESC"
							,long_desc = "prefix.user.change"
							,argument_help = "PREFIX.USER.CHANGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,optional_arguments_type = "string"
							,function = prefixUserChange
						)
						,Command(
							name = "clear"
							,short_desc = "PREFIX.USER.CLEAR.SHORTDESC"
							,function = prefixUserClear
						)
					]
				)
			]
		)
		,Command(
			name = "settings"
			,short_desc = "SETTINGS.SHORTDESC"
			,sub_commands = [
				Command(
					name = "server"
					,short_desc = "SETTINGS.SERVER.SHORTDESC"
					,server_only = True
					,default_permissions = [
						"manage_guild"
					]
					,sub_commands = [
						Command(
							name = "permissions"
							,short_desc = "SETTINGS.SERVER.PERMISSIONS.SHORTDESC"
							,sub_commands = [
								Command(
									name = "give"
									,short_desc = "SETTINGS.SERVER.PERMISSIONS.GIVE.SHORTDESC"
									,long_desc = "settings.server.permissions.give"
									,argument_help = "SETTINGS.SERVER.PERMISSIONS.GIVE.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsServerPermissionsGive
								)
								,Command(
									name = "deny"
									,short_desc = "SETTINGS.SERVER.PERMISSIONS.DENY.SHORTDESC"
									,long_desc = "settings.server.permissions.deny"
									,argument_help = "SETTINGS.SERVER.PERMISSIONS.DENY.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsServerPermissionsDeny
								)
								,Command(
									name = "undo"
									,short_desc = "SETTINGS.SERVER.PERMISSIONS.UNDO.SHORTDESC"
									,long_desc = "settings.server.permissions.undo"
									,argument_help = "SETTINGS.SERVER.PERMISSIONS.UNDO.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsServerPermissionsUndo
								)
								,Command(
									name = "clear"
									,short_desc = "SETTINGS.SERVER.PERMISSIONS.CLEAR.SHORTDESC"
									,long_desc = "settings.server.permissions.clear"
									,argument_help = "SETTINGS.SERVER.PERMISSIONS.CLEAR.ARGUMENTS"
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
							,short_desc = "SETTINGS.SERVER.LANGUAGE.SHORTDESC"
							,sub_commands = [
								Command(
									name = "change"
									,short_desc = "SETTINGS.SERVER.LANGUAGE.CHANGE.SHORTDESC"
									,long_desc = "settings.server.language.change"
									,argument_help = "SETTINGS.SERVER.LANGUAGE.CHANGE.ARGUMENTS"
									,argument_types = [
										"string"
									]
									,optional_arguments_type = "string"
									,function = changeServerLanguage
								)
								,Command(
									name = "clear"
									,short_desc = "SETTINGS.SERVER.LANGUAGE.CLEAR.SHORTDESC"
									,function = clearServerLanguage
								)
							]
						)
						,Command(
							name = "sync_with"
							,short_desc = "SETTINGS.SERVER.SYNC_WITH.SHORTDESC"
							,long_desc = "settings.server.sync_with"
							,argument_help = "SETTINGS.SERVER.SYNC_WITH.ARGUMENTS"
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
					,short_desc = "SETTINGS.CHANNEL.SHORTDESC"
					,server_only = True
					,default_permissions = [
						"manage_guild"
					]
					,sub_commands = [
						Command(
							name = "permissions"
							,short_desc = "SETTINGS.CHANNEL.PERMISSIONS.SHORTDESC"
							,sub_commands = [
								Command(
									name = "give"
									,short_desc = "SETTINGS.CHANNEL.PERMISSIONS.GIVE.SHORTDESC"
									,long_desc = "settings.channel.permissions.give"
									,argument_help = "SETTINGS.CHANNEL.PERMISSIONS.GIVE.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsChannelPermissionsGive
								)
								,Command(
									name = "deny"
									,short_desc = "SETTINGS.CHANNEL.PERMISSIONS.DENY.SHORTDESC"
									,long_desc = "settings.channel.permissions.deny"
									,argument_help = "SETTINGS.CHANNEL.PERMISSIONS.DENY.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsChannelPermissionsDeny
								)
								,Command(
									name = "undo"
									,short_desc = "SETTINGS.CHANNEL.PERMISSIONS.UNDO.SHORTDESC"
									,long_desc = "settings.channel.permissions.undo"
									,argument_help = "SETTINGS.CHANNEL.PERMISSIONS.UNDO.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,optional_arguments_type = "string"
									,function = settingsChannelPermissionsUndo
								)
								,Command(
									name = "clear"
									,short_desc = "SETTINGS.CHANNEL.PERMISSIONS.CLEAR.SHORTDESC"
									,long_desc = "settings.channel.permissions.clear"
									,argument_help = "SETTINGS.CHANNEL.PERMISSIONS.CLEAR.ARGUMENTS"
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
							,short_desc = "SETTINGS.CHANNEL.LANGUAGE.SHORTDESC"
							,sub_commands = [
								Command(
									name = "change"
									,short_desc = "SETTINGS.CHANNEL.LANGUAGE.CHANGE.SHORTDESC"
									,long_desc = "settings.channel.language.change"
									,argument_help = "SETTINGS.CHANNEL.LANGUAGE.CHANGE.ARGUMENTS"
									,argument_types = [
										"string"
									]
									,optional_arguments_type = "string"
									,function = changeChannelLanguage
								)
								,Command(
									name = "clear"
									,short_desc = "SETTINGS.CHANNEL.LANGUAGE.CLEAR.SHORTDESC"
									,function = clearChannelLanguage
								)
							]
						)
						,Command(
							name = "sync"
							,short_desc = "SETTINGS.CHANNEL.SYNC.SHORTDESC"
							,default_permissions = [
								"administrator"
							]
							,sub_commands = [
								Command(
									name = "add"
									,short_desc = "SETTINGS.CHANNEL.SYNC.ADD.SHORTDESC"
									,long_desc = "settings.channel.sync.add"
									,argument_help = "SETTINGS.CHANNEL.SYNC.ADD.ARGUMENTS"
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
									,short_desc = "SETTINGS.CHANNEL.SYNC.DEL.SHORTDESC"
									,long_desc = "settings.channel.sync.del"
									,argument_help = "SETTINGS.CHANNEL.SYNC.DEL.ARGUMENTS"
									,optional_arguments_type = "string"
									,default_permissions = [
										"administrator"
									]
									,function = channelUnsync
								)
								,Command(
									name = "view"
									,short_desc = "SETTINGS.CHANNEL.SYNC.VIEW.SHORTDESC"
									,long_desc = "settings.channel.sync.view"
									,function = channelSyncView
								)
							]
						)
					]
				)
				,Command(
					name = "user"
					,short_desc = "SETTINGS.USER.SHORTDESC"
					,sub_commands = [
						Command(
							name = "language"
							,short_desc = "SETTINGS.USER.LANGUAGE.SHORTDESC"
							,sub_commands = [
								Command(
									name = "change"
									,short_desc = "SETTINGS.USER.LANGUAGE.CHANGE.SHORTDESC"
									,long_desc = "settings.user.language.change"
									,argument_help = "SETTINGS.USER.LANGUAGE.CHANGE.ARGUMENTS"
									,argument_types = [
										"string"
									]
									,optional_arguments_type = "string"
									,function = changeUserLanguage
								)
								,Command(
									name = "clear"
									,short_desc = "SETTINGS.USER.LANGUAGE.CLEAR.SHORTDESC"
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
			,short_desc = "INFO.SHORTDESC"
			,sub_commands = [
				Command(
					name = "permissions"
					,short_desc = "INFO.PERMISSIONS.SHORTDESC"
					,server_only = True
					,function = infoPermissions
				)
			]
		)
		,Command(
			name = "lewd"
			,short_desc = "LEWD.SHORTDESC"
			,function = lewd
			,nsfw_function = nsfwLewd
		)
	]
)

ioScripts.saveCommandsPickle(commands)