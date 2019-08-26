"""Information-related commands."""
from discord import Embed

from aid import dates
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
    return True


async def get_command_info(context, arguments):
    """Get command info of a specific command."""
    command = arguments[0]

    aliases = await context.language.get_string_list(
        command.localisation[context.language_id]["names"][1:])

    if aliases == "":
        aliases = await context.language.get_text("no_aliases")

    platforms = ["category", "channel", "guild", "user", "global"]
    command_use_times = {}
    for platform in platforms:
        platform_cmd_data = getattr(getattr(context, platform + "_data"), "command_data")
        command_data = await platform_cmd_data.get_object_from_id_path(command.id_path)

        language_key = "command_" + platform + "_uses_"
        number = await context.language.format_number(command_data.use_times)
        number = "**" + number + "**"
        if command_data.use_times == 1:
            language_key += "singular"
        else:
            language_key += "plural"

        command_use_times[platform] = await context.language.get_text(
            language_key, {"times": number})

    basic_info = (
        "{aliases_title}: **{aliases_content}**\n"
        "{command_use_times[global]}\n"
        "{command_use_times[guild]}\n"
        "{command_use_times[category]}\n"
        "{command_use_times[channel]}\n"
        "{command_use_times[user]}").format(
            aliases_title=await context.language.get_text("command_aliases_title"),
            aliases_content=aliases, command_use_times=command_use_times)

    related_commands = ""
    for command in command.related_commands:
        if related_commands:
            related_commands += "\n"

        related_commands += await command.get_command_string(
            context, include_prefix=False)

    sub_commands = await command.get_sub_commands(context, filter_unallowed=False)

    sub_commands_string = ""
    for sub_command in sub_commands:
        if sub_commands_string:
            sub_commands_string += "\n"

        sub_command_name = await sub_command.get_command_string(
            context, include_prefix=False)

        sub_commands_string += (
            sub_command_name.split(".")[-1] + " - " +
            sub_command.localisation[context.language_id]["description"])

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "command_info_title",
            {"command": await command.get_command_string(context, include_prefix=False)}),
        embeds.EmbedFieldCollection(
            basic_info, await context.language.get_text("basic_command_info_title")))

    if sub_commands_string:
        message.fields.append(embeds.EmbedFieldCollection(
            sub_commands_string, await context.language.get_text("sub_commands_title")))

    if related_commands:
        message.fields.append(embeds.EmbedFieldCollection(
            related_commands, await context.language.get_text("related_commands_title")))

    for i, argument in enumerate(command.arguments):
        message.fields.append(await argument.get_info_embed_field(context, i + 1))

    message.embed.title = command.localisation[context.language_id]["description"]
    message.embed.description = command.localisation[context.language_id]["help_text"]

    await message.send(context)
    return True
