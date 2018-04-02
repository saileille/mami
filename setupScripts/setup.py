from Command import *
from commandFunctions import *
import ioScripts

commands = Command(
	name = "head"
	,all_prefixes = True
	,sub_commands = [
		Command(
			name = "test"
			,short_desc = "COMMAND.TEST.SHORTDESC"
			,long_desc = "test"
			,function = test
		)
		,Command(
			name = "prefix"
			,short_desc = "COMMAND.PREFIX.SHORTDESC"
			,all_prefixes = True
			,sub_commands = [
				Command(
					name = "view"
					,short_desc = "COMMAND.PREFIX.VIEW.SHORTDESC"
					,long_desc = "prefix.view"
					,all_prefixes = True
					,function = prefixView
				)
				,Command(
					name = "server"
					,short_desc = "COMMAND.PREFIX.SERVER.SHORTDESC"
					,sub_commands = [
						Command(
							name = "change"
							,short_desc = "COMMAND.PREFIX.SERVER.CHANGE.SHORTDESC"
							,long_desc = "prefix.server.change"
							,argument_help = "COMMAND.PREFIX.SERVER.CHANGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,function = prefixServerChange
						)
						,Command(
							name = "clear"
							,short_desc = "COMMAND.PREFIX.SERVER.CLEAR.SHORTDESC"
							,long_desc = "prefix.server.clear"
							,function = prefixServerClear
						)
					]
				)
				,Command(
					name = "channel"
					,short_desc = "COMMAND.PREFIX.CHANNEL.SHORTDESC"
					,sub_commands = [
						Command(
							name = "change"
							,short_desc = "COMMAND.PREFIX.CHANNEL.CHANGE.SHORTDESC"
							,long_desc = "prefix.channel.change"
							,argument_help = "COMMAND.PREFIX.CHANNEL.CHANGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,function = prefixChannelChange
						)
						,Command(
							name = "clear"
							,short_desc = "COMMAND.PREFIX.CHANNEL.CLEAR.SHORTDESC"
							,long_desc = "prefix.channel.clear"
							,function = prefixChannelClear
						)
					]
				)
				,Command(
					name = "user"
					,short_desc = "COMMAND.PREFIX.USER.SHORTDESC"
					,sub_commands = [
						Command(
							name = "change"
							,short_desc = "COMMAND.PREFIX.USER.CHANGE.SHORTDESC"
							,long_desc = "prefix.user.change"
							,argument_help = "COMMAND.PREFIX.USER.CHANGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,function = prefixUserChange
						)
						,Command(
							name = "clear"
							,short_desc = "COMMAND.PREFIX.USER.CLEAR.SHORTDESC"
							,long_desc = "prefix.user.clear"
							,function = prefixUserClear
						)
					]
				)
			]
		)
		,Command(
			name = "settings"
			,short_desc = "COMMAND.SETTINGS.SHORTDESC"
			,sub_commands = [
				Command(
					name = "server"
					,short_desc = "COMMAND.SETTINGS.SERVER.SHORTDESC"
					,default_permissions = [
						"manage_server"
					]
					,sub_commands = [
						Command(
							name = "permissions"
							,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.SHORTDESC"
							,sub_commands = [
								Command(
									name = "give"
									,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.GIVE.SHORTDESC"
									,long_desc = "settings.server.permissions.give"
									,argument_help = "COMMAND.SETTINGS.SERVER.PERMISSIONS.GIVE.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsServerPermissionsGive
								)
								,Command(
									name = "deny"
									,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.DENY.SHORTDESC"
									,long_desc = "settings.server.permissions.deny"
									,argument_help = "COMMAND.SETTINGS.SERVER.PERMISSIONS.DENY.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsServerPermissionsDeny
								)
								,Command(
									name = "undo"
									,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.UNDO.SHORTDESC"
									,long_desc = "settings.server.permissions.undo"
									,argument_help = "COMMAND.SETTINGS.SERVER.PERMISSIONS.UNDO.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsServerPermissionsUndo
								)
								,Command(
									name = "clear"
									,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.CLEAR.SHORTDESC"
									,long_desc = "settings.server.permissions.clear"
									,argument_help = "COMMAND.SETTINGS.SERVER.PERMISSIONS.CLEAR.ARGUMENTS"
									,argument_types = [
										"string"
									]
									,function = settingsServerPermissionsClear
								)
							]
						)
						,Command(
							name = "language"
							,short_desc = "COMMAND.SETTINGS.SERVER.LANGUAGE.SHORTDESC"
							,long_desc = "settings.server.language"
							,argument_help = "COMMAND.SETTINGS.SERVER.LANGUAGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,function = serverLanguage
						)
					]
				)
				,Command(
					name = "channel"
					,short_desc = "COMMAND.SETTINGS.CHANNEL.SHORTDESC"
					,default_permissions = [
						"manage_server"
					]
					,sub_commands = [
						Command(
							name = "permissions"
							,short_desc = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.SHORTDESC"
							,sub_commands = [
								Command(
									name = "give"
									,short_desc = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.GIVE.SHORTDESC"
									,long_desc = "settings.channel.permissions.give"
									,argument_help = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.GIVE.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsChannelPermissionsGive
								)
								,Command(
									name = "deny"
									,short_desc = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.DENY.SHORTDESC"
									,long_desc = "settings.channel.permissions.deny"
									,argument_help = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.DENY.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsChannelPermissionsDeny
								)
								,Command(
									name = "undo"
									,short_desc = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.UNDO.SHORTDESC"
									,long_desc = "settings.channel.permissions.undo"
									,argument_help = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.UNDO.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsChannelPermissionsUndo
								)
								,Command(
									name = "clear"
									,short_desc = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.CLEAR.SHORTDESC"
									,long_desc = "settings.channel.permissions.clear"
									,argument_help = "COMMAND.SETTINGS.CHANNEL.PERMISSIONS.CLEAR.ARGUMENTS"
									,argument_types = [
										"string"
									]
									,function = settingsChannelPermissionsClear
								)
							]
						)
						,Command(
							name = "language"
							,short_desc = "COMMAND.SETTINGS.CHANNEL.LANGUAGE.SHORTDESC"
							,long_desc = "settings.channel.language"
							,argument_help = "COMMAND.SETTINGS.CHANNEL.LANGUAGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,function = channelLanguage
						)
					]
				)
				,Command(
					name = "user"
					,short_desc = "COMMAND.SETTINGS.USER.SHORTDESC"
					,sub_commands = [
						Command(
							name = "language"
							,short_desc = "COMMAND.SETTINGS.USER.LANGUAGE.SHORTDESC"
							,long_desc = "settings.user.language"
							,argument_help = "COMMAND.SETTINGS.USER.LANGUAGE.ARGUMENTS"
							,argument_types = [
								"string"
							]
							,function = userLanguage
						)
					]
				)
			]
		)
		,Command(
			name = "info"
			,short_desc = "COMMAND.INFO.SHORTDESC"
			,sub_commands = [
				Command(
					name = "permissions"
					,short_desc = "COMMAND.INFO.PERMISSIONS.SHORTDESC"
					,long_desc = "info.permissions"
					,function = infoPermissions
				)
			]
		)
	]
)

ioScripts.saveCommandsPickle(commands)