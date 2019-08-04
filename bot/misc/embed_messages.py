"""discord.Embed-building and sending."""
from framework import embeds


async def invalid_argument(context, argument, custom_msg=None):
    """Send invalid argument feedback message."""
    message = embeds.PaginatedEmbed(
        await context.language.get_text("invalid_argument_title"),
        embeds.EmbedFieldCollection(
            custom_msg,
            await context.language.get_text("invalid_argument_custom_msg_title")))

    message.embed.description = "❌ " + await context.language.get_text(
        "invalid_argument_desc", {"arg": argument})

    await message.send(context)


async def too_many_arguments(context, argument_count, argument):
    """Send too many arguments feedback message."""
    message = embeds.PaginatedEmbed(
        await context.language.get_text("too_many_arguments_title"))

    desc = None
    if argument_count == 1:
        desc = await context.language.get_text(
            "too_many_arguments_singular_desc", {"arg": argument, "args": argument_count})
    else:
        desc = await context.language.get_text(
            "too_many_arguments_plural_desc", {"arg": argument, "args": argument_count})

    message.embed.description = "❌ " + desc
    await message.send(context)


async def no_action(context, commands, command_string):
    """Send a feedback message when the command called has no method to call."""
    message = embeds.PaginatedEmbed(
        await context.language.get_text("no_action_title"), embeds.EmbedFieldCollection(
            commands, await context.language.get_text("command")))

    message.embed.description = "ℹ " + await context.language.get_text(
        "no_action_desc", {"command": command_string})

    await message.send(context)


async def invalid_command_subcommands(
        context, commands, command_string, last_working_command_string):
    """
    Feedback message.

    Send a feedback message when an invalid command was called, and the last valid
    one has sub-commands.
    """
    message = embeds.PaginatedEmbed(
        await context.language.get_text("invalid_command_title"),
        embeds.EmbedFieldCollection(
            commands, await context.language.get_text("command")))

    message.embed.description = "❌ " + await context.language.get_text(
        "invalid_command_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await message.send(context)


async def invalid_command_no_subcommands(
        context, command_string, last_working_command_string):
    """
    Feedback message.

    Send a feedback message when an invalid command was called, and the last valid
    one does not have sub-commands.
    """
    message = embeds.PaginatedEmbed(
        await context.language.get_text("invalid_command_title"))

    message.embed.description = "❌ " + await context.language.get_text(
        "invalid_command_no_subcommands_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await message.send(context)


async def not_authorised(context, command_string, last_working_command_string):
    """
    Feedback message.

    Send a feedback message when the user has attempted to use a command which they
    cannot use.
    """
    message = embeds.PaginatedEmbed(
        await context.language.get_text("unauthorised_command_title"))

    message.embed.description = "🚫 " + await context.language.get_text(
        "unauthorised_command_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await message.send(context)


async def no_usable_sub_commands(context, command_string, last_working_command_string):
    """
    Feedback message.

    Send a feedback message when the user attempts to use a command with no usable
    sub-commands.
    """
    message = embeds.PaginatedEmbed(
        await context.language.get_text("no_usable_sub_commands_title"))

    message.embed.description = ":exclamation: " + await context.language.get_text(
        "no_usable_sub_commands_desc",
        {"command": command_string, "last_working": last_working_command_string})

    await message.send(context)


async def failed_pre_check(context, custom_msg):
    """Send a failed pre-check feedback message."""
    message = embeds.PaginatedEmbed(
        await context.language.get_text("failed_pre_check_title"),
        embeds.EmbedFieldCollection(
            custom_msg, await context.language.get_text("failed_pre_check_custom_msg_title")))

    message.embed.description = ":grey_exclamation: " + await context.language.get_text(
        "failed_pre_check_desc")

    await message.send(context)
