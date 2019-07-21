"""Shortcut-related conversions."""
from bot.data import definitions
from bot.misc import embed_messages


async def find_shortcut_name(argument, context, platform_type, condition):
    """
    Find if shortcut name exists on any given platform.

    Helper function.
    """
    platform = getattr(context, platform_type + "_data")
    return (argument in platform.shortcuts) == condition


async def not_guild_shortcut_name(argument, context):
    """
    Check if the argument is not an existing guild shortcut name.

    If the guild shortcut name is not in use, return argument.
    """
    if await find_shortcut_name(argument, context, "guild", False):
        return argument

    custom_msg = await context.language.get_text("existing_guild_shortcut_name")
    await embed_messages.invalid_argument(context, argument, custom_msg)

    return None


async def guild_shortcut_name(argument, context, verbose=True):
    """
    Check if the argument is an existing guild shortcut name.

    If the guild shortcut name is in use, return argument.
    """
    if await find_shortcut_name(argument, context, "guild", True):
        return argument

    if verbose:
        custom_msg = await context.language.get_text("not_guild_shortcut_name")
        await embed_messages.invalid_argument(context, argument, custom_msg)

    return None


async def not_channel_shortcut_name(argument, context):
    """
    Check if the argument is not an existing channel shortcut name.

    If the channel shortcut name is not in use, return argument.
    """
    if await find_shortcut_name(argument, context, "channel", False):
        return argument

    return None


async def channel_shortcut_name(argument, context):
    """
    Check if the argument is an existing channel shortcut name.

    If the channel shortcut name is in use, return argument.
    """
    if await find_shortcut_name(argument, context, "channel", True):
        return argument

    return None


async def not_user_shortcut_name(argument, context):
    """
    Check if the argument is not an existing user shortcut name.

    If the user shortcut name is not in use, return argument.
    """
    if await find_shortcut_name(argument, context, "user", False):
        return argument

    return None


async def user_shortcut_name(argument, context):
    """
    Check if the argument is an existing user shortcut name.

    If the user shortcut name is in use, return argument.
    """
    if await find_shortcut_name(argument, context, "user", True):
        return argument

    return None


async def any_shortcut(argument, context):
    """
    Check if the argument is any existing shortcut name.

    If the argument is a shortcut name, return shortcut.
    """
    shortcut = None

    if await user_shortcut_name(argument, context):
        shortcut = context.user_data.shortcuts[argument]
    elif await channel_shortcut_name(argument, context):
        shortcut = context.channel_data.shortcuts[argument]
    elif await guild_shortcut_name(argument, context, verbose=False):
        shortcut = context.guild_data.shortcuts[argument]
    else:
        guild_shortcut = await definitions.COMMANDS.get_sub_command_from_path(
            ["settings", "guild", "shortcut", "add"])

        """category_shortcut = await definitions.COMMANDS.get_sub_command_from_path(
            ["settings", "category", "shortcut", "add"])

        channel_shortcut = await definitions.COMMANDS.get_sub_command_from_path(
            ["settings", "channel", "shortcut", "add"])

        user_shortcut = await definitions.COMMANDS.get_sub_command_from_path(
            ["settings", "user", "shortcut", "add"])"""

        guild_shortcut_cmd = await guild_shortcut.get_command_string(context)
        """category_shortcut_cmd = await category_shortcut.get_command_string(context)
        channel_shortcut_cmd = await channel_shortcut.get_command_string(context)
        user_shortcut_cmd = await user_shortcut.get_command_string(context)"""

        custom_msg = await context.language.get_text("invalid_shortcut_name")
        custom_msg += "\n\n:information_source: " + await context.language.get_text(
            "invalid_shortcut_name_info", {"guild_shortcut": guild_shortcut_cmd})

        await embed_messages.invalid_argument(context, argument, custom_msg)

    return shortcut
