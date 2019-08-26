"""Import stuff."""
from bot.data import definitions
from framework import exceptions
from framework.command_input import CommandInput


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


async def get_command(command_list, context, check_allowance=True):
    """
    Check if command exists and if the user is allowed to use it.

    Return both the command, and the last working command, in case the command
    resulted in an error.
    """
    command = definitions.COMMANDS
    last_working_command = command

    for command_call in command_list:
        for sub_command in command.sub_commands.values():
            if command_call in sub_command.localisation[context.language_id]["names"]:
                exception = None
                if check_allowance:
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


async def process_command_call(context, command_string):
    """
    Process the command call.

    Contains everything from the moment prefix has been determined as valid.
    """
    command_input = CommandInput(command_string)
    await command_input.parse_raw_text()

    command, last_working_command = await get_command(command_input.commands, context)

    if command == exceptions.InvalidCommandException:
        await last_working_command.invalid_command(context, command_input)
        return

    if command == exceptions.CommandCheckException:
        await last_working_command.not_authorised(context, command_input)
        return

    if command == exceptions.PreCheckException:
        # The feedback message has already been handled.
        return

    if command == exceptions.NoExecutableSubCommands:
        await last_working_command.no_usable_sub_commands(context, command_input)
        return

    if await command.execute(context, command_input):
        await context.add_command_use(command.id_path)
