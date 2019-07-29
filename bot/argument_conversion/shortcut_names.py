"""Shortcut-related conversions."""
from bot.data import definitions
from bot.misc import embed_messages


async def is_not_shortcut_name(argument, context, platform_type, verbose):
    """Check that a shortcut with given name does not exist on given platform."""
    data_object = getattr(context, platform_type + "_data")
    if argument not in data_object.shortcuts:
        return argument

    if verbose:
        custom_msg = await context.language.get_text(
            "existing_" + platform_type + "_shortcut_name")

        await embed_messages.invalid_argument(context, argument, custom_msg)

    return None


async def is_not_category_shortcut_name(argument, context, verbose=True):
    """Check that the argument is not an existing category shortcut name."""
    return await is_not_shortcut_name(argument, context, "category", verbose)


async def is_not_channel_shortcut_name(argument, context, verbose=True):
    """Check that the argument is not an existing channel shortcut name."""
    return await is_not_shortcut_name(argument, context, "channel", verbose)


async def is_not_guild_shortcut_name(argument, context, verbose=True):
    """Check that the argument is not an existing guild shortcut name."""
    return await is_not_shortcut_name(argument, context, "guild", verbose)


async def is_not_user_shortcut_name(argument, context, verbose=True):
    """Check that the argument is not an existing user shortcut name."""
    return await is_not_shortcut_name(argument, context, "user", verbose)


async def is_shortcut_name(argument, context, platform_type, verbose):
    """Check that a shortcut with given name exists on given platform."""
    data_object = getattr(context, platform_type + "_data")
    if argument in data_object.shortcuts:
        return argument

    if verbose:
        custom_msg = await context.language.get_text(
            "not_" + platform_type + "_shortcut_name")

        await embed_messages.invalid_argument(context, argument, custom_msg)

    return None


async def is_category_shortcut_name(argument, context, verbose=True):
    """Check that the argument is an existing category shortcut name."""
    return await is_shortcut_name(argument, context, "category", verbose)


async def is_channel_shortcut_name(argument, context, verbose=True):
    """Check that the argument is an existing channel shortcut name."""
    return await is_shortcut_name(argument, context, "channel", verbose)


async def is_guild_shortcut_name(argument, context, verbose=True):
    """Check that the argument is an existing guild shortcut name."""
    return await is_shortcut_name(argument, context, "guild", verbose)


async def is_user_shortcut_name(argument, context, verbose=True):
    """Check that the argument is an existing user shortcut name."""
    return await is_shortcut_name(argument, context, "user", verbose)


async def any_shortcut(argument, context):
    """
    Check if the argument is any existing shortcut name.

    If the argument is a shortcut name, return shortcut.
    """
    shortcut = None
    check_order = ["user", "channel", "category", "guild"]
    for name in check_order:
        shortcuts = None
        try:
            shortcuts = getattr(context, name + "_data").shortcuts
        except AttributeError:
            continue

        if argument in shortcuts:
            shortcut = shortcuts[argument]
            break

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
