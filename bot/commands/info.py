"""Information-related commands."""
import discord

from aid import dates
from framework import embeds


async def guild_member_info(context, command_input):
    """Show basic information of a member."""
    member = command_input.arguments[0]

    join_time = member.joined_at.strftime(
        await context.get_language_text("datetime_format"))
    time_in_guild = await dates.get_time_difference_string(context, member.joined_at)
    join_data = await context.get_language_text(
        "datetime_and_time_passed", {"datetime": join_time, "time_passed": time_in_guild})

    creation_time = member.created_at.strftime(
        await context.get_language_text("datetime_format"))
    time_on_discord = await dates.get_time_difference_string(context, member.created_at)
    creation_data = await context.get_language_text(
        "datetime_and_time_passed",
        {"datetime": creation_time, "time_passed": time_on_discord})

    embed = discord.Embed()
    embed.description = await context.get_language_text(
        "member_info_desc", {"member": member.display_name})

    embed.add_field(
        name=await context.get_language_text(
            "member_info_discord_name"), value=member.name)
    embed.add_field(
        name=await context.get_language_text(
            "member_info_creation_time"), value=creation_data)
    embed.add_field(
        name=await context.get_language_text(
            "member_info_join_time", {"guild": member.guild.name}), value=join_data)
    embed.add_field(
        name=await context.get_language_text(
            "member_info_top_role"), value=member.top_role.name)

    await embeds.send(
        context, await context.get_language_text(
            "member_info_title", {"name": member.display_name}),
        embed, thumbnail=member.avatar_url, colour=member.colour)
