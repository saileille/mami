"""Setting-related commands and functions."""
from bot.database import database_functions
from framework import embeds


async def set_language(context, arguments, platform):
    """Set language."""
    platform_data = getattr(context, platform + "_data")

    platform_data.language_id = arguments[0]
    await database_functions.update_language(context, platform)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text(platform + "_language_updated_title"))

    confirmation_text = platform_data.language.flag_emoji
    if confirmation_text is None:
        confirmation_text = "✅"

    message.embed.description = confirmation_text + " " + (
        await context.language.get_text(
            platform + "_language_updated_desc",
            {"language": context.language.get_language_name(
                platform_data.language.obj_id)}))

    await message.send(context)
    return True


async def set_category_language(context, arguments):
    """Set the category language."""
    return await set_language(context, arguments, "category")


async def set_channel_language(context, arguments):
    """Set the channel language."""
    return await set_language(context, arguments, "channel")


async def set_guild_language(context, arguments):
    """Set the guild language."""
    return await set_language(context, arguments, "guild")


async def set_user_language(context, arguments):
    """Set the user language."""
    return await set_language(context, arguments, "user")


async def reset_language(context, platform):
    """Reset a language."""
    platform_data = getattr(context, platform + "_data")

    platform_data.language_id = None
    await database_functions.update_language(context, platform)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text(platform + "_language_reset_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        platform + "_language_reset_desc")

    await message.send(context)
    return True


async def reset_category_language(context, arguments):
    """Reset the category language."""
    return await reset_language(context, "category")


async def reset_channel_language(context, arguments):
    """Reset the channel language."""
    return await reset_language(context, "channel")


async def reset_guild_language(context, arguments):
    """Reset the guild language."""
    return await reset_language(context, "guild")


async def reset_user_language(context, arguments):
    """Reset the user language."""
    return await reset_language(context, "user")


async def add_command_rule(context, arguments, platform, ruletype):
    """Add any type of command rule."""
    command_data_objects = arguments[0]
    rules = arguments[1:]

    for command_data in command_data_objects:
        for rule in rules:
            await command_data["data"].command_rules.add_rule(rule, ruletype)

    await database_functions.update_command_data(context, platform)

    message = embeds.PaginatedEmbed(
        await context.language.get_text(platform + "_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        platform + "_command_rules_added_desc")

    await message.send(context)
    return True


async def add_inclusionary_category_command_rule(context, arguments):
    """Add inclusionary command rules to category."""
    return await add_command_rule(context, arguments, "category", "inclusionary")


async def add_inclusionary_channel_command_rule(context, arguments):
    """Add inclusionary command rules to channel."""
    return await add_command_rule(context, arguments, "channel", "inclusionary")


async def add_inclusionary_guild_command_rule(context, arguments):
    """Add inclusionary command rules to guild."""
    return await add_command_rule(context, arguments, "guild", "inclusionary")


async def add_exclusionary_category_command_rule(context, arguments):
    """Add exclusionary command rules to category."""
    return await add_command_rule(context, arguments, "category", "exclusionary")


async def add_exclusionary_channel_command_rule(context, arguments):
    """Add exclusionary command rules to channel."""
    return await add_command_rule(context, arguments, "channel", "exclusionary")


async def add_exclusionary_guild_command_rule(context, arguments):
    """Add exclusionary command rules to guild."""
    return await add_command_rule(context, arguments, "guild", "exclusionary")


async def remove_command_rule(context, arguments, platform):
    """Remove command rules."""
    command_data_objects = arguments[0]
    rules = arguments[1:]

    for command_data in command_data_objects:
        for rule in rules:
            await command_data["data"].command_rules.remove_rule(rule)

    await database_functions.update_command_data(context, platform)

    message = embeds.PaginatedEmbed(
        await context.language.get_text(platform + "_command_rules_removed_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        platform + "_command_rules_removed_desc")

    await message.send(context)
    return True


async def remove_category_command_rule(context, arguments):
    """Remove command rules from category."""
    return await remove_command_rule(context, arguments, "category")


async def remove_channel_command_rule(context, arguments):
    """Remove command rules from channel."""
    return await remove_command_rule(context, arguments, "channel")


async def remove_guild_command_rule(context, arguments):
    """Remove command rules from guild."""
    return await remove_command_rule(context, arguments, "guild")


async def display_command_rules(context, arguments, platform):
    """Display command rules on any platform."""
    command_data = arguments[0]

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "display_" + platform + "_command_rules_title",
            {"command": command_data["name"]}))

    command_rules = command_data["data"].command_rules

    message.embed.description = await context.language.get_text(
        "display_" + platform + "_command_rules_" + command_rules.type + "_rules_desc")

    members = []
    for member_id in command_rules.users:
        member = context.message.guild.get_member(member_id)
        member_name = None

        if member is not None:
            member_name = "{member.display_name} ({member.id})".format(member=member)
        else:
            member_name = "[{former_member}] ({id})".format(
                former_member=await context.language.get_text("former_guild_member"),
                id=member_id)

        members.append(member_name)

    roles = []
    for role_id in command_rules.roles:
        role = context.message.guild.get_role(role_id)
        role_name = None
        if role is not None:
            role_name = "{role.name} ({role.id})".format(role=role)
        else:
            role_name = "[{former_role}] ({id})".format(
                former_role=await context.language.get_text("former_guild_role"),
                id=role_id)

        roles.append(role_name)

    permissions = []
    if command_rules.permissions is not None:
        for permission_code in command_rules.permissions:
            permissions.append(context.language.permission_names[permission_code])

    if members:
        message.fields.append(embeds.EmbedFieldCollection(
            members, await context.language.get_text("members_title")))

    if roles:
        message.fields.append(embeds.EmbedFieldCollection(
            roles, await context.language.get_text("roles_title")))

    if permissions:
        message.fields.append(embeds.EmbedFieldCollection(
            permissions, await context.language.get_text("permissions_title")))

    await message.send(context)
    return True


async def display_category_command_rules(context, arguments):
    """Display one command's command rules for category."""
    return await display_command_rules(context, arguments, "category")


async def display_channel_command_rules(context, arguments):
    """Display one command's command rules for channel."""
    return await display_command_rules(context, arguments, "channel")


async def display_guild_command_rules(context, arguments):
    """Display one command's command rules for guild."""
    return await display_command_rules(context, arguments, "guild")
