from Command import *
from commandFunctions import *
import ioScripts

commands = [
	Command(
		name = "COMMAND.TEST.NAME"
		,short_desc = "COMMAND.TEST.SHORTDESC"
		,long_desc = "COMMAND.TEST.LONGDESC"
		,function = test
	)
]

ioScripts.saveCommandsPickle(commands)