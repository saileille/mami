"""Anything related to converting command names."""
from bot.data import data_functions
from bot.misc import embed_messages


async def command_to_guild_command_rules(argument, context):
    """
    Check if the argument is a valid command name.

    If valid, return the Checks object for the guild of that command.
    """
    id_path = await data_functions.get_id_path_from_command_name(argument, context)
    if id_path is None:
        return None

    return await context.guild_data.checks.get_object_from_id_path(id_path)


async def commands_to_guild_command_rules(argument, context):
    """
    Check if the argument consists of valid command names.

    If valid, return a list of Checks objects for the guild of that command.
    """
    command_names = argument.split(" ")
    command_rules = []

    for command_name in command_names:
        id_path = await data_functions.get_id_path_from_command_name(command_name,
                                                                     context)
        if id_path is None:
            custom_msg = await context.language.get_text(
                "invalid_command_name", {"cmd_name": command_name})

            await embed_messages.invalid_argument(
                context, argument, custom_msg)

            return None

        command_rule = await context.guild_data.checks.get_object_from_id_path(id_path)
        command_rules.append(command_rule)

    return command_rules


async def commands_to_guild_allow_command_rules(argument, context):
    """
    Check if argument has commands to which allow rules can be added.

    If any command specified has deny rules attached to it, the argument is invalid.
    If valid, return a list of Checks object for the guild of that command.
    """
    command_rules = await commands_to_guild_command_rules(argument, context)

    if command_rules is None:
        return command_rules

    for i, command_rule in enumerate(command_rules):
        if not command_rule.deny.is_empty:
            command_names = argument.split(" ")
            custom_msg = await context.language.get_text(
                "command_has_deny_rules", {"cmd_name": context.prefix + command_names[i]})

            await embed_messages.invalid_argument(context, argument, custom_msg)

            return None

    return command_rules
