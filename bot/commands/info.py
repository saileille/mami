"""Information-related commands."""
from discord import Embed

from aid import dates
from aid import strings
from framework import embeds


async def guild_member_info(context, arguments):
    """Show basic information of a member."""
    member = arguments[0]

    join_time = member.joined_at.strftime(
        await context.language.get_text("datetime_format"))
    time_in_guild = await dates.get_time_difference_string(context, member.joined_at)
    join_data = await context.language.get_text(
        "datetime_and_time_passed", {"datetime": join_time, "time_passed": time_in_guild})

    creation_time = member.created_at.strftime(
        await context.language.get_text("datetime_format"))
    time_on_discord = await dates.get_time_difference_string(context, member.created_at)
    creation_data = await context.language.get_text(
        "datetime_and_time_passed",
        {"datetime": creation_time, "time_passed": time_on_discord})

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "member_info_title", {"name": member.display_name}),
        embeds.EmbedFieldCollection(
            member.name, await context.language.get_text("member_info_discord_name")),
        embeds.EmbedFieldCollection(
            creation_data, await context.language.get_text("member_info_creation_time")),
        embeds.EmbedFieldCollection(
            join_data, await context.language.get_text(
                "member_info_join_time", {"guild": member.guild.name})),
        embeds.EmbedFieldCollection(
            member.top_role.name, await context.language.get_text(
                "member_info_top_role")))

    message.embed.description = await context.language.get_text(
        "member_info_desc", {"member": member.display_name})

    colour = member.colour
    if str(colour) == "#000000":
        colour = Embed.Empty

    await message.send(context, thumbnail=member.avatar_url, colour=colour)


async def get_command_info(context, arguments):
    """Get command info of a specific command."""
    command = arguments[0]

    aliases = await context.language.get_string_list(
        command.localisation[context.language_id]["names"][1:])

    if aliases == "":
        aliases = await context.language.get_text("no_aliases")

    basic_info = (
        "**{aliases_title}**: {aliases_content}\n"
        "**{has_sub_commands_title}**: {has_sub_commands_content}").format(
            aliases_title=await context.language.get_text("command_aliases_title"),
            aliases_content=aliases,
            has_sub_commands_title=await context.language.get_text(
                "command_has_sub_commands_title"),
            has_sub_commands_content=await strings.get_yes_no_emojis(
                bool(command.sub_commands)))

    related_commands = ""
    for command in command.related_commands:
        if related_commands:
            related_commands += "\n"
        related_commands += command.get_command_string(context, include_prefix=False)

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "command_info_title",
            {"command": await command.get_command_string(context, include_prefix=False)}),
        embeds.EmbedFieldCollection(
            basic_info, await context.language.get_text("basic_command_info_title")))

    if related_commands:
        message.fields.append(embeds.EmbedFieldCollection(
            related_commands, await context.language.get_text("related_commands_title")))

    for i, argument in enumerate(command.arguments):
        message.fields.append(await argument.get_info_embed_field(context, i + 1))

    message.embed.description = command.localisation[context.language_id]["description"]

    await message.send(context)
