"""Anything related to converting command names."""
from bot.data import data_functions
from bot.misc import embed_messages
from framework import command_handler
from framework import exceptions


async def command_to_command_object(argument, context, verbose=True):
    """Get the command object from a command name without prefix."""
    command, last_working = await command_handler.get_command(
        argument.split("."), context, check_allowance=False)

    if command == exceptions.InvalidCommandException:
        command = None
        if verbose:
            await embed_messages.invalid_argument(
                context, argument, await context.language.get_text(
                    "invalid_command_name", {"cmd_name": argument}))

    return command


async def command_to_command_data(argument, context, data_object, verbose):
    """
    Check if the argument is a valid command name.

    Helper function. If valid, return the CommandData object for channel, category or
    guild.
    """
    id_path = await data_functions.get_id_path_from_command_name(argument, context)

    if id_path is None:
        if verbose:
            custom_msg = await context.language.get_text(
                "invalid_command_name", {"cmd_name": argument})

            await embed_messages.invalid_argument(
                context, argument, custom_msg)

        return None

    return {
        "data": await data_object.command_data.get_object_from_id_path(id_path),
        "name": argument}


async def command_to_category_command_data(argument, context, verbose=True):
    """Convert command name to category command data."""
    return await command_to_command_data(
        argument, context, context.category_data, verbose)


async def command_to_channel_command_data(argument, context, verbose=True):
    """Convert command name to channel command data."""
    return await command_to_command_data(argument, context, context.channel_data, verbose)


async def command_to_guild_command_data(argument, context, verbose=True):
    """Convert command name to guild command data."""
    return await command_to_command_data(argument, context, context.guild_data, verbose)


async def command_to_non_empty_command_rules(argument, context, data_object, verbose):
    """Convert command name to command data that has some command rules."""
    argument = await command_to_command_data(argument, context, data_object, verbose)

    if argument is not None:
        if argument["data"].command_rules.is_empty:
            if verbose:
                custom_msg = await context.language.get_text(
                    "display_category_command_rules_no_command_rules")

                await embed_messages.invalid_argument(
                    context, argument["name"], custom_msg)

            argument = None

    return argument


async def command_to_non_empty_category_command_rules(argument, context, verbose=True):
    """Convert command name to non-empty category command rules."""
    return await command_to_non_empty_command_rules(
        argument, context, context.category_data, verbose)


async def command_to_non_empty_channel_command_rules(argument, context, verbose=True):
    """Convert command name to non-empty channel command rules."""
    return await command_to_non_empty_command_rules(
        argument, context, context.channel_data, verbose)


async def command_to_non_empty_guild_command_rules(argument, context, verbose=True):
    """Convert command name to non-empty guild command rules."""
    return await command_to_non_empty_command_rules(
        argument, context, context.guild_data, verbose)


async def commands_to_command_data(argument, context, data_object, verbose):
    """
    Check if the argument consists of valid command names.

    If valid, return a list of CommandData objects for channel, category or guild of that
    command.
    """
    command_names = argument.split(" ")
    command_data_objects = []

    for command_name in command_names:
        command_data = await command_to_command_data(
            command_name, context, data_object, verbose=False)

        if command_data is None:
            if verbose:
                custom_msg = await context.language.get_text(
                    "invalid_command_name", {"cmd_name": command_name})

                await embed_messages.invalid_argument(context, argument, custom_msg)

            return None

        command_data_objects.append(command_data)

    return command_data_objects


async def commands_to_category_command_data(argument, context):
    """Convert command names to category command data."""
    return await commands_to_command_data(
        argument, context, context.category_data, verbose=True)


async def commands_to_channel_command_data(argument, context):
    """Convert command names to channel command data."""
    return await commands_to_command_data(
        argument, context, context.channel_data, verbose=True)


async def commands_to_guild_command_data(argument, context):
    """Convert command names to guild command data."""
    return await commands_to_command_data(
        argument, context, context.guild_data, verbose=True)


async def commands_to_inclusionary_or_exclusionary_command_rules(
        argument, context, data_object, not_of_type, verbose):
    """
    Check that argument has commands to which rules of chosen type can be added.

    If any command specified has not_of_type rules attached to it, the argument is
    invalid. If valid, return a list of CommandData object for channel, category or guild
    of that command.
    """
    command_data_objects = await commands_to_command_data(
        argument, context, data_object, verbose)

    if command_data_objects is None:
        return None

    for command_data in command_data_objects:
        command_rules = command_data["data"].command_rules
        if command_rules.type == not_of_type and not command_rules.is_empty:
            if verbose:
                custom_msg = await context.language.get_text(
                    "command_has_" + not_of_type + "_rules",
                    {"cmd_name": command_data["name"]})

                await embed_messages.invalid_argument(context, argument, custom_msg)

            return None

    return command_data_objects


async def commands_to_inclusionary_command_rules(argument, context, data_object, verbose):
    """Check if argument has commands to which inclusionary rules can be added."""
    return await commands_to_inclusionary_or_exclusionary_command_rules(
        argument, context, data_object, "exclusionary", verbose)


async def commands_to_category_inclusionary_command_rules(argument, context):
    """Category-specific version."""
    return await commands_to_inclusionary_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_channel_inclusionary_command_rules(argument, context):
    """Channel-specific version."""
    return await commands_to_inclusionary_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_guild_inclusionary_command_rules(argument, context):
    """Guild-specific version."""
    return await commands_to_inclusionary_command_rules(
        argument, context, context.guild_data, verbose=True)


async def commands_to_exclusionary_command_rules(argument, context, data_object, verbose):
    """Check if argument has commands to which exclusionary rules can be added."""
    return await commands_to_inclusionary_or_exclusionary_command_rules(
        argument, context, data_object, "inclusionary", verbose)


async def commands_to_category_exclusionary_command_rules(argument, context):
    """Category-specific version."""
    return await commands_to_exclusionary_command_rules(
        argument, context, context.category_data, verbose=True)


async def commands_to_channel_exclusionary_command_rules(argument, context):
    """Channel-specific version."""
    return await commands_to_exclusionary_command_rules(
        argument, context, context.channel_data, verbose=True)


async def commands_to_guild_exclusionary_command_rules(argument, context):
    """Guild-specific version."""
    return await commands_to_exclusionary_command_rules(
        argument, context, context.guild_data, verbose=True)
