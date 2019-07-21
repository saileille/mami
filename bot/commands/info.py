"""Information-related commands."""
from aid import dates
from framework import embeds


async def guild_member_info(context, command_input):
    """Show basic information of a member."""
    member = command_input.arguments[0]

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

    await message.send(context, thumbnail=member.avatar_url, colour=member.colour)
