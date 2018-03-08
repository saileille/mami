from Command import *
from commandFunctions import *
import ioScripts

commands = [
	Command(
		name = "COMMAND.TEST.NAME"
		,short_desc = "COMMAND.TEST.SHORTDESC"
		,long_desc = "test"
		,function = test
	)
	,Command(
		name = "COMMAND.PREFIX.NAME"
		,short_desc = "COMMAND.PREFIX.SHORTDESC"
		,long_desc = "prefix"
		,all_prefixes = True
		,sub_commands = [
			Command(
				name = "COMMAND.PREFIX.VIEW.NAME"
				,short_desc = "COMMAND.PREFIX.VIEW.SHORTDESC"
				,long_desc = "prefix.view"
				,function = prefixView
			)
			,Command(
				name = "COMMAND.PREFIX.USER.NAME"
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
]

ioScripts.saveCommandsPickle(commands)