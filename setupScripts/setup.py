from Command import *
from commandFunctions import *
import ioScripts

commands = Command(
	name = "root"
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
					name = "user"
					,short_desc = "COMMAND.PREFIX.USER.SHORTDESC"
					,long_desc = "prefix.user"
					,min_arguments = 1
					,argument_help = "COMMAND.PREFIX.USER.ARGUMENTS"
					,argument_types = [
						"string"
					]
					,function = prefixUser
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
					,sub_commands = [
						Command(
							name = "permissions"
							,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.SHORTDESC"
							,sub_commands = [
								Command(
									name = "give"
									,short_desc = "COMMAND.SETTINGS.SERVER.PERMISSIONS.GIVE.SHORTDESC"
									,long_desc = "settings.server.permissions.give"
									,min_arguments = 2
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
									,min_arguments = 2
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
									,min_arguments = 2
									,argument_help = "COMMAND.SETTINGS.SERVER.PERMISSIONS.UNDO.ARGUMENTS"
									,argument_types = [
										"string"
										,"string"
									]
									,function = settingsServerPermissionsUndo
								)
							]
						)
					]
				)
			]
		)
	]
)

ioScripts.saveCommandsPickle(commands)