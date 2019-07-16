"""Setting-related commands and functions."""
import discord

from bot.database import database_functions
from framework import embeds


async def set_category_language(context, command_input):
    """Set the category language."""
    context.category_data.language_id = command_input.arguments[0]
    await database_functions.update_category_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    confirmation_text = context.category_data.language.flag_emojis
    if not confirmation_text:
        confirmation_text = ":white_check_mark:"

    embed.description = confirmation_text + " " + (
        await context.get_language_text(
            "category_language_updated_desc",
            {"language": await context.language.get_language(
                context.category_data.language.obj_id)}))

    await embeds.send(
        context, await context.get_language_text("category_language_updated_title"),
        embed)


async def set_channel_language(context, command_input):
    """Set the channel language."""
    context.channel_data.language_id = command_input.arguments[0]
    await database_functions.update_channel_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    confirmation_text = context.channel_data.language.flag_emojis
    if not confirmation_text:
        confirmation_text = ":white_check_mark:"

    embed.description = confirmation_text + " " + (
        await context.get_language_text(
            "channel_language_updated_desc",
            {"language": await context.language.get_language(
                context.channel_data.language.obj_id)}))

    await embeds.send(
        context, await context.get_language_text("channel_language_updated_title"), embed)


async def set_guild_language(context, command_input):
    """Set the guild language."""
    context.guild_data.language_id = command_input.arguments[0]
    await database_functions.update_guild_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    confirmation_text = context.guild_data.language.flag_emojis
    if not confirmation_text:
        confirmation_text = ":white_check_mark:"

    embed.description = confirmation_text + " " + (
        await context.get_language_text(
            "guild_language_updated_desc",
            {"language": await context.language.get_language(
                context.guild_data.language.obj_id)}))

    await embeds.send(
        context, await context.get_language_text("guild_language_updated_title"), embed)


async def set_user_language(context, command_input):
    """Set the user language."""
    context.user_data.language_id = command_input.arguments[0]
    await database_functions.update_user_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    embed.description = context.user_data.language.flag_emojis + " " + (
        await context.get_language_text(
            "user_language_updated_desc",
            {"language": await context.language.get_language(
                context.user_data.language.obj_id)}))

    await embeds.send(
        context, await context.get_language_text("user_language_updated_title"), embed)


async def reset_category_language(context, command_input):
    """Reset the category language."""
    context.category_data.language_id = None
    await database_functions.update_category_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    embed.description = ":white_check_mark: " + (
        await context.get_language_text("category_language_reset_desc"))

    await embeds.send(
        context, await context.get_language_text("category_language_reset_title"), embed)


async def reset_channel_language(context, command_input):
    """Reset the channel language."""
    context.channel_data.language_id = None
    await database_functions.update_channel_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    embed.description = ":white_check_mark: " + (
        await context.get_language_text("channel_language_reset_desc"))

    await embeds.send(
        context, await context.get_language_text("channel_language_reset_title"), embed)


async def reset_guild_language(context, command_input):
    """Reset the guild language."""
    context.guild_data.language_id = None
    await database_functions.update_guild_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    embed.description = ":white_check_mark: " + (
        await context.get_language_text("guild_language_reset_desc"))

    await embeds.send(
        context, await context.get_language_text("guild_language_reset_title"), embed)


async def reset_user_language(context, command_input):
    """Reset the user language."""
    context.user_data.language_id = None
    await database_functions.update_user_language(context)
    await context.clear_cache()

    embed = discord.Embed()

    embed.description = ":white_check_mark: " + (
        await context.get_language_text("user_language_reset_desc"))

    await embeds.send(
        context, await context.get_language_text("user_language_reset_title"), embed)


async def add_allow_guild_check(context, command_input):
    """Add allowing command rules to guild."""
    check_objects = command_input.arguments[0]
    rule_additions = command_input.arguments[1:]

    for rule_addition in rule_additions:
        rule_type = None
        if isinstance(rule_addition, discord.Member):
            rule_type = "member"
        elif isinstance(rule_addition, discord.Role):
            rule_type = "role"
        elif isinstance(rule_addition, str):
            rule_type = "permission"

        for check_object in check_objects:
            await check_object.allow.add_rule(rule_addition, rule_type)

    await database_functions.update_guild_checks(context)

    print(str(context.guild_data.checks))
