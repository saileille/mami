"""Import stuff."""
from bot.data import definitions
from framework import exceptions


class CommandHandler():
    """Various static methods related to handling commands."""

    @staticmethod
    async def check_prefix(context):
        """
        Check if message has the appropriate prefix.

        If prefix exists, return the message without prefix.
        If prefix does not exist, return None.
        """
        prefix = context.prefix
        content = context.message.content

        command = None
        if content.startswith(prefix):
            command = content[len(prefix):]

        return command

    @staticmethod
    async def get_command(command_input, context):
        """
        Check if command exists and if the user is allowed to use it.

        Return both the command, and the last working command, in case the command
        resulted in an error.
        """
        command = definitions.COMMANDS
        last_working_command = command

        for command_call in command_input.commands:
            for sub_command in command.sub_commands.values():
                if command_call in sub_command.localisation[context.language_id]["names"]:
                    exception = await sub_command.check_if_allowed(context)
                    if exception is None:
                        command = sub_command
                        last_working_command = command
                    else:
                        return exception, last_working_command

                    break
            else:
                # If a command was not found...
                command = exceptions.InvalidCommandException
                break

        return command, last_working_command
