"""Anything related to converting command names."""
from bot.data import data_functions
from bot.misc import embed_messages


async def command_to_command_rules(argument, context, data_object, verbose):
    """
    Check if the argument is a valid command name.

    Helper function. If valid, return the CommandRules object for channel, category or
    guild.
    """
    id_path = await data_functions.get_id_path_from_command_name(argument, context)

    if id_path is None and verbose:
        custom_msg = await context.language.get_text(
            "invalid_command_name", {"cmd_name": argument})

        await embed_messages.invalid_argument(
            context, argument, custom_msg)

        return None

    return {
        "rule": await data_object.command_rules.get_object_from_id_path(id_path),
        "name": argument}


async def command_to_category_command_rules(argument, context, verbose=True):
    """Convert command name to category command rules."""
    return command_to_command_rules(argument, context, context.category_data, verbose)


async def command_to_channel_command_rules(argument, context, verbose=True):
    """Convert command name to channel command rules."""
    return command_to_command_rules(argument, context, context.channel_data, verbose)


async def command_to_guild_command_rules(argument, context, verbose=True):
    """Convert command name to guild command rules."""
    return command_to_command_rules(argument, context, context.guild_data, verbose)


async def commands_to_command_rules(argument, context, data_object, verbose):
    """
    Check if the argument consists of valid command names.

    If valid, return a list of CommandRules objects for channel, category or guild of that
    command.
    """
    command_names = argument.split(" ")
    command_rules = []

    for command_name in command_names:
        command_rule = await command_to_command_rules(
            command_name, context, data_object, verbose=False)

        if command_rule is None:
            if verbose:
                custom_msg = await context.language.get_text(
                    "invalid_command_name", {"cmd_name": command_name})

                await embed_messages.invalid_argument(
                    context, argument, custom_msg)

            return None

        command_rules.append(command_rule)

    return command_rules


async def commands_to_category_command_rules(argument, context):
    """Convert command names to category command rules."""
    return commands_to_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_channel_command_rules(argument, context):
    """Convert command names to channel command rules."""
    return commands_to_command_rules(
        argument, context, context.channel_data, verbose=True)


async def commands_to_guild_command_rules(argument, context):
    """Convert command names to guild command rules."""
    return commands_to_command_rules(argument, context, context.guild_data, verbose=True)


async def commands_to_inclusionary_command_rules(argument, context, data_object, verbose):
    """
    Check if argument has commands to which inclusionary rules can be added.

    If any command specified has exclusionary rules attached to it, the argument is
    invalid. If valid, return a list of CommandRules object for channel, category or guild
    of that command.
    """
    command_rules = await commands_to_command_rules(
        argument, context, data_object, verbose)

    if command_rules is None:
        return None

    for command_rule in command_rules:
        if not command_rule["rule"].exclusionary.is_empty:
            if verbose:
                custom_msg = await context.language.get_text(
                    "command_has_exclusionary_rules", {"cmd_name": command_rule["name"]})

                await embed_messages.invalid_argument(context, argument, custom_msg)

            return None

    return command_rules


async def commands_to_category_inclusionary_command_rules(argument, context):
    """Category-specific version."""
    return commands_to_inclusionary_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_channel_inclusionary_command_rules(argument, context):
    """Channel-specific version."""
    return commands_to_inclusionary_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_guild_inclusionary_command_rules(argument, context):
    """Guild-specific version."""
    return commands_to_inclusionary_command_rules(
        argument, context, context.guild_data, verbose=True)


async def commands_to_exclusionary_command_rules(argument, context, data_object, verbose):
    """
    Check if argument has commands to which exclusionary rules can be added.

    If any command specified has inclusionary rules attached to it, the argument is
    invalid. If valid, return a list of dictionaries containing CommandRules objects and
    names for the channel, category or guild of that command.
    """
    command_rules = await commands_to_command_rules(
        argument, context, data_object, verbose)

    if command_rules is None:
        return None

    for command_rule in command_rules:
        if not command_rule["rule"].inclusionary.is_empty:
            custom_msg = await context.language.get_text(
                "command_has_inclusionary_rules", {"cmd_name": command_rule["name"]})

            await embed_messages.invalid_argument(context, argument, custom_msg)

            return None

    return command_rules


async def commands_to_category_exclusionary_command_rules(argument, context):
    """Category-specific version."""
    return commands_to_exclusionary_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_channel_exclusionary_command_rules(argument, context):
    """Channel-specific version."""
    return commands_to_exclusionary_command_rules(
        argument, context, context.channel_data, verbose=True)


async def commands_to_guild_exclusionary_command_rules(argument, context):
    """Guild-specific version."""
    return commands_to_exclusionary_command_rules(
        argument, context, context.guild_data, verbose=True)
