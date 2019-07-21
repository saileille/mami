"""
Pre-checks for commands, unrelated to permissions and the like.

If command can be used, return True.
If command cannot be used, return False. Also send a message explaining why the command
cannot be used at the time.
"""
from bot.misc import embed_messages
from bot.data import definitions


async def in_dms(context, verbose):
    """Make sure the command is used in direct messages."""
    msg_in_dms = context.guild_data is None

    if not msg_in_dms and verbose:
        custom_msg = await context.language.get_text("command_used_in_guild")
        await embed_messages.failed_pre_check(context, custom_msg)

    return msg_in_dms


async def in_guild(context, verbose):
    """Make sure the command is used in a guild."""
    msg_in_guild = context.guild_data is not None

    if not msg_in_guild and verbose:
        custom_msg = await context.language.get_text("command_used_in_dms")
        await embed_messages.failed_pre_check(context, custom_msg)

    return msg_in_guild


async def guild_has_shortcuts(context, verbose):
    """Check if the guild has at least one shortcut."""
    has_shortcuts = bool(context.guild_data.shortcuts)

    if not has_shortcuts and verbose:
        shortcut_cmd = await definitions.COMMANDS.get_sub_command_from_path(
            ["settings", "guild", "shortcut", "add"])

        shortcut_cmd_name = await shortcut_cmd.get_command_string(context)

        custom_msg = await context.language.get_text(
            "no_guild_shortcuts", {"shortcut_cmd": shortcut_cmd_name})

        await embed_messages.failed_pre_check(context, custom_msg)

    return has_shortcuts


async def category_has_language(context, verbose):
    """Check if the guild has a language set."""
    has_language = context.category_data.language_id is not None

    if not has_language and verbose:
        custom_msg = await context.language.get_text("no_set_category_language")
        await embed_messages.failed_pre_check(context, custom_msg)

    return has_language


async def channel_has_language(context, verbose):
    """Check if the guild has a language set."""
    has_language = context.channel_data.language_id is not None

    if not has_language and verbose:
        custom_msg = await context.language.get_text("no_set_channel_language")
        await embed_messages.failed_pre_check(context, custom_msg)

    return has_language


async def guild_has_language(context, verbose):
    """Check if the guild has a language set."""
    has_language = context.guild_data.language_id is not None

    if not has_language and verbose:
        custom_msg = await context.language.get_text("no_set_guild_language")
        await embed_messages.failed_pre_check(context, custom_msg)

    return has_language


async def user_has_language(context, verbose):
    """Check if the guild has a language set."""
    has_language = context.user_data.language_id is not None

    if not has_language and verbose:
        custom_msg = await context.language.get_text("no_set_user_language")
        await embed_messages.failed_pre_check(context, custom_msg)

    return has_language
