"""
Pre-checks for commands, unrelated to command rules.

If command can be used, return True.
If command cannot be used, return False. Also send a message explaining why the command
cannot be used at the time.
"""
from bot.misc import embed_messages
from bot.data import definitions


async def in_dms(context, verbose=True):
    """Make sure the command is used in direct messages."""
    msg_in_dms = context.guild_data is None

    if not msg_in_dms and verbose:
        await embed_messages.failed_pre_check(
            context, await context.language.get_text("command_used_in_guild"))

    return msg_in_dms


async def in_guild(context, verbose=True):
    """Make sure the command is used in a guild."""
    msg_in_guild = context.guild_data is not None

    if not msg_in_guild and verbose:
        await embed_messages.failed_pre_check(
            context, await context.language.get_text("command_used_in_dms"))

    return msg_in_guild


async def in_category(context, verbose=True):
    """Make sure the command is used on a channel that has category."""
    pre_check = context.category_data is not None

    if not pre_check and verbose:
        await embed_messages.failed_pre_check(
            context, await context.language.get_text("command_used_in_category"))

    return pre_check


async def platform_has_shortcuts(context, platform_type, verbose):
    """Check if the given platform has at least one shortcut."""
    data_object = getattr(context, platform_type + "_data")
    has_shortcuts = bool(data_object.shortcuts)

    if not has_shortcuts and verbose:
        shortcut_cmd = definitions.COMMANDS.get_sub_command_from_path(
            "settings", platform_type, "shortcut", "add")

        shortcut_cmd_name = await shortcut_cmd.get_command_string(context)

        custom_msg = await context.language.get_text(
            "no_" + platform_type + "_shortcuts", {"shortcut_cmd": shortcut_cmd_name})

        await embed_messages.failed_pre_check(context, custom_msg)

    return has_shortcuts


async def category_has_shortcuts(context, verbose=True):
    """Check if the category has at least one shortcut."""
    return await platform_has_shortcuts(context, "category", verbose)


async def channel_has_shortcuts(context, verbose=True):
    """Check if the channel has at least one shortcut."""
    return await platform_has_shortcuts(context, "channel", verbose)


async def guild_has_shortcuts(context, verbose=True):
    """Check if the guild has at least one shortcut."""
    return await platform_has_shortcuts(context, "guild", verbose)


async def user_has_shortcuts(context, verbose=True):
    """Check if the user has at least one shortcut."""
    return await platform_has_shortcuts(context, "user", verbose)


async def platform_has_language(context, platform_type, verbose):
    """Check if the platform has a language set."""
    data_object = getattr(context, platform_type + "_data")
    has_language = data_object.language_id is not None

    if not has_language and verbose:
        custom_msg = await context.language.get_text(
            "no_set_" + platform_type + "_language")

        await embed_messages.failed_pre_check(context, custom_msg)

    return has_language


async def category_has_language(context, verbose=True):
    """Check if the category has a language set."""
    return await platform_has_language(context, "category", verbose)


async def channel_has_language(context, verbose=True):
    """Check if the channel has a language set."""
    return await platform_has_language(context, "channel", verbose)


async def guild_has_language(context, verbose=True):
    """Check if the guild has a language set."""
    return await platform_has_language(context, "guild", verbose)


async def user_has_language(context, verbose=True):
    """Check if the user has a language set."""
    return await platform_has_language(context, "user", verbose)


async def is_not_connecting_guild_call(context, verbose=True):
    """Check that the channel is not connecting for a call."""
    pre_check = (await in_guild(context, verbose=False) and
                 not context.channel_data.guild_call.connecting and
                 context.channel_data.guild_call.connected_channel is None)

    if not pre_check and verbose:
        await embed_messages.failed_pre_check(
            context, await context.language.get_text("is_connecting_guild_call"))

    return pre_check


async def is_connecting_or_connected_guild_call(context, verbose=True):
    """Check that the channel is connecting or connected for a call."""
    pre_check = (await in_guild(context, verbose=False) and
                 context.channel_data.guild_call.connecting or
                 context.channel_data.guild_call.connected_channel is not None)

    if not pre_check and verbose:
        await embed_messages.failed_pre_check(
            context, await context.language.get_text(
                "is_not_connecting_connected_guild_call"))

    return pre_check
