"""discord.Embed-building and sending."""
import discord

from framework import embeds


async def invalid_argument(context, argument, custom_msg=None):
    """Send invalid argument feedback message."""
    embed = discord.Embed()

    embed.description = ":x: " + await context.get_language_text(
        "invalid_argument_desc", {"arg": argument})

    if custom_msg is not None:
        embed.add_field(
            name=await context.get_language_text("invalid_argument_custom_msg_title"),
            value=custom_msg)

    await embeds.send(
        context, await context.get_language_text("invalid_argument_title"), embed)


async def too_many_arguments(context, argument_count, argument):
    """Send too many arguments feedback message."""
    embed = discord.Embed()

    desc = None
    if argument_count == 1:
        desc = await context.get_language_text(
            "too_many_arguments_singular_desc", {"arg": argument, "args": argument_count})
    else:
        desc = await context.get_language_text(
            "too_many_arguments_plural_desc", {"arg": argument, "args": argument_count})

    embed.description = ":x: " + desc

    await embeds.send(
        context, await context.get_language_text("too_many_arguments_title"), embed)


async def no_action(context, commands, command_string):
    """Send a feedback message when the command called has no method to call."""
    embed = discord.Embed()

    embed.description = ":information_source: " + await context.get_language_text(
        "no_action_desc", {"command": command_string})

    embed.add_field(
        name=await context.get_language_text("command"), value="\n".join(commands))

    await embeds.send(
        context, await context.get_language_text("no_action_title"), embed)


async def invalid_command_subcommands(context, commands, command_string,
                                      last_working_command_string):
    """
    Feedback message.

    Send a feedback message when an invalid command was called, and the last valid
    one has sub-commands.
    """
    embed = discord.Embed()
    embed.description = ":x: " + await context.get_language_text(
        "invalid_command_desc",
        {"command": command_string, "last_working": last_working_command_string})

    embed.add_field(
        name=await context.get_language_text("command"), value="\n".join(commands))

    await embeds.send(
        context, await context.get_language_text("invalid_command_title"), embed)


async def invalid_command_no_subcommands(context, command_string,
                                         last_working_command_string):
    """
    Feedback message.

    Send a feedback message when an invalid command was called, and the last valid
    one does not have sub-commands.
    """
    embed = discord.Embed()
    embed.description = ":x: " + await context.get_language_text(
        "invalid_command_no_subcommands_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await embeds.send(
        context, await context.get_language_text("invalid_command_title"), embed)


async def not_authorised(context, command_string, last_working_command_string):
    """
    Feedback message.

    Send a feedback message when the user has attempted to use a command which they
    cannot use.
    """
    embed = discord.Embed()
    embed.description = ":no_entry_sign: " + await context.get_language_text(
        "unauthorised_command_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await embeds.send(
        context, await context.get_language_text("unauthorised_command_title"), embed)


async def no_usable_sub_commands(context, command_string, last_working_command_string):
    """
    Feedback message.

    Send a feedback message when the user attempts to use a command with no usable
    sub-commands.
    """
    embed = discord.Embed()
    embed.description = ":exclamation: " + await context.get_language_text(
        "no_usable_sub_commands_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await embeds.send(
        context, await context.get_language_text("no_usable_sub_commands_title"), embed)


async def failed_pre_check(context, custom_msg):
    """Send a failed pre-check feedback message."""
    embed = discord.Embed()
    embed.description = await context.get_language_text("failed_pre_check_desc")
    embed.description = ":grey_exclamation: " + embed.description

    embed.add_field(
        name=await context.get_language_text("failed_pre_check_custom_msg_title"),
        value=custom_msg)

    await embeds.send(
        context, await context.get_language_text("failed_pre_check_title"), embed)
