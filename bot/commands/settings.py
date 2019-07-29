"""Setting-related commands and functions."""
from bot.database import database_functions
from framework import embeds


async def set_category_language(context, arguments):
    """Set the category language."""
    context.category_data.language_id = arguments[0]
    await database_functions.update_category_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("category_language_updated_title"))

    confirmation_text = context.category_data.language.flag_emoji
    if confirmation_text is None:
        confirmation_text = "✅"

    message.embed.description = confirmation_text + " " + (
        await context.language.get_text(
            "category_language_updated_desc",
            {"language": await context.language.get_language(
                context.category_data.language.obj_id)}))

    await message.send(context)


async def set_channel_language(context, arguments):
    """Set the channel language."""
    context.channel_data.language_id = arguments[0]
    await database_functions.update_channel_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("channel_language_updated_title"))

    confirmation_text = context.channel_data.language.flag_emoji
    if confirmation_text is None:
        confirmation_text = "✅"

    message.embed.description = confirmation_text + " " + (
        await context.language.get_text(
            "channel_language_updated_desc",
            {"language": await context.language.get_language(
                context.channel_data.language.obj_id)}))

    await message.send(context)


async def set_guild_language(context, arguments):
    """Set the guild language."""
    context.guild_data.language_id = arguments[0]
    await database_functions.update_guild_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_language_updated_title"))

    confirmation_text = context.guild_data.language.flag_emoji
    if confirmation_text is None:
        confirmation_text = "✅"

    message.embed.description = confirmation_text + " " + (
        await context.language.get_text(
            "guild_language_updated_desc",
            {"language": await context.language.get_language(
                context.guild_data.language.obj_id)}))

    await message.send(context)


async def set_user_language(context, arguments):
    """Set the user language."""
    context.user_data.language_id = arguments[0]
    await database_functions.update_user_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("user_language_updated_title"))

    confirmation_text = context.guild_data.language.flag_emoji
    if confirmation_text is None:
        confirmation_text = "✅"

    message.embed.description = confirmation_text + " " + (
        await context.language.get_text(
            "user_language_updated_desc",
            {"language": await context.language.get_language(
                context.user_data.language.obj_id)}))

    await message.send(context)


async def reset_category_language(context, arguments):
    """Reset the category language."""
    context.category_data.language_id = None
    await database_functions.update_category_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("category_language_reset_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "category_language_reset_desc")

    await message.send(context)


async def reset_channel_language(context, arguments):
    """Reset the channel language."""
    context.channel_data.language_id = None
    await database_functions.update_channel_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("channel_language_reset_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "channel_language_reset_desc")

    await message.send(context)


async def reset_guild_language(context, arguments):
    """Reset the guild language."""
    context.guild_data.language_id = None
    await database_functions.update_guild_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_language_reset_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "guild_language_reset_desc")

    await message.send(context)


async def reset_user_language(context, arguments):
    """Reset the user language."""
    context.user_data.language_id = None
    await database_functions.update_user_language(context)
    await context.clear_cache()

    message = embeds.PaginatedEmbed(
        await context.language.get_text("user_language_reset_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "user_language_reset_desc")

    await message.send(context)


async def add_inclusionary_category_command_rule(context, arguments):
    """Add inclusionary command rules to category."""
    command_rule_objects = arguments[0]
    rule_additions = arguments[1:]

    for rule_addition in rule_additions:
        for command_rule_object in command_rule_objects:
            await command_rule_object["rule"].inclusionary.add_rule(rule_addition)

    await database_functions.update_category_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("category_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "category_command_rules_added_desc")

    await message.send(context)


async def add_inclusionary_channel_command_rule(context, arguments):
    """Add inclusionary command rules to channel."""
    command_rule_objects = arguments[0]
    rule_additions = arguments[1:]

    for rule_addition in rule_additions:
        for command_rule_object in command_rule_objects:
            await command_rule_object["rule"].inclusionary.add_rule(rule_addition)

    await database_functions.update_channel_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("channel_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "channel_command_rules_added_desc")

    await message.send(context)


async def add_inclusionary_guild_command_rule(context, arguments):
    """Add inclusionary command rules to guild."""
    command_rule_objects = arguments[0]
    rule_additions = arguments[1:]

    for rule_addition in rule_additions:
        for command_rule_object in command_rule_objects:
            await command_rule_object["rule"].inclusionary.add_rule(rule_addition)

    await database_functions.update_guild_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "guild_command_rules_added_desc")

    await message.send(context)


async def add_exclusionary_category_command_rule(context, arguments):
    """Add exclusionary command rules to category."""
    command_rule_objects = arguments[0]
    rule_additions = arguments[1:]

    for command_rule_object in command_rule_objects:
        for rule_addition in rule_additions:
            await command_rule_object["rule"].exclusionary.add_rule(rule_addition)

    await database_functions.update_category_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("category_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "category_command_rules_added_desc")

    await message.send(context)


async def add_exclusionary_channel_command_rule(context, arguments):
    """Add exclusionary command rules to channel."""
    command_rule_objects = arguments[0]
    rule_additions = arguments[1:]

    for command_rule_object in command_rule_objects:
        for rule_addition in rule_additions:
            await command_rule_object["rule"].exclusionary.add_rule(rule_addition)

    await database_functions.update_channel_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("channel_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "channel_command_rules_added_desc")

    await message.send(context)


async def add_exclusionary_guild_command_rule(context, arguments):
    """Add exclusionary command rules to guild."""
    command_rule_objects = arguments[0]
    rule_additions = arguments[1:]

    for command_rule_object in command_rule_objects:
        for rule_addition in rule_additions:
            await command_rule_object["rule"].exclusionary.add_rule(rule_addition)

    await database_functions.update_guild_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_command_rules_added_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "guild_command_rules_added_desc")

    await message.send(context)


async def remove_category_command_rule(context, arguments):
    """Remove command rules from category."""
    command_rule_objects = arguments[0]
    rules = arguments[1:]

    for command_rule_object in command_rule_objects:
        for rule in rules:
            await command_rule_object["rule"].remove_rule(rule)

    await database_functions.update_category_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("category_command_rules_removed_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "category_command_rules_removed_desc")

    await message.send(context)


async def remove_channel_command_rule(context, arguments):
    """Remove command rules from channel."""
    command_rule_objects = arguments[0]
    rules = arguments[1:]

    for command_rule_object in command_rule_objects:
        for rule in rules:
            await command_rule_object["rule"].remove_rule(rule)

    await database_functions.update_channel_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("channel_command_rules_removed_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "channel_command_rules_removed_desc")

    await message.send(context)


async def remove_guild_command_rule(context, arguments):
    """Remove command rules from guild."""
    command_rule_objects = arguments[0]
    rules = arguments[1:]

    for command_rule_object in command_rule_objects:
        for rule in rules:
            await command_rule_object["rule"].remove_rule(rule)

    await database_functions.update_guild_command_rules(context)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_command_rules_removed_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        "guild_command_rules_removed_desc")

    await message.send(context)


async def display_category_command_rules(context, arguments):
    """Display one command's command rules for category."""
    command_rule_object = arguments[0]

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "display_category_command_rules_title",
            {"command": command_rule_object["name"]}))

    command_rule_set_type = None
    if not command_rule_object["rule"].inclusionary.is_empty:
        command_rule_set_type = "inclusionary"

    elif not command_rule_object["rule"].exclusionary.is_empty:
        command_rule_set_type = "exclusionary"

    else:
        message.embed.description = await context.language.get_text(
            "display_category_command_rules_no_command_rules")

        await message.send(context)
        return

    command_rule_set = getattr(command_rule_object["rule"], command_rule_set_type)
    message.embed.description = await context.language.get_text(
        "display_category_command_rules_" + command_rule_set_type + "_rules_desc")

    members = []
    for member_id in command_rule_set.users:
        member = context.message.category.get_member(member_id)
        member_name = None

        if member is not None:
            member_name = "{member.display_name} ({member.id})".format(member=member)
        else:
            member_name = "[{former_member}] ({id})".format(
                former_member=await context.language.get_text("former_category_member"),
                id=member_id)

        members.append(member_name)

    roles = []
    for role_id in command_rule_set.roles:
        role = context.message.category.get_role(role_id)
        role_name = None
        if role is not None:
            role_name = "{role.name} ({role.id})".format(role=role)
        else:
            role_name = "[{former_role}] ({id})".format(
                former_role=await context.language.get_text("former_category_role"),
                id=role_id)

        roles.append(role_name)

    permissions = []
    if command_rule_set.permissions is not None:
        for permission_code in command_rule_set.permissions:
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


async def display_channel_command_rules(context, arguments):
    """Display one command's command rules for channel."""
    command_rule_object = arguments[0]

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "display_channel_command_rules_title",
            {"command": command_rule_object["name"]}))

    command_rule_set_type = None
    if not command_rule_object["rule"].inclusionary.is_empty:
        command_rule_set_type = "inclusionary"

    elif not command_rule_object["rule"].exclusionary.is_empty:
        command_rule_set_type = "exclusionary"

    else:
        message.embed.description = await context.language.get_text(
            "display_channel_command_rules_no_command_rules")

        await message.send(context)
        return

    command_rule_set = getattr(command_rule_object["rule"], command_rule_set_type)
    message.embed.description = await context.language.get_text(
        "display_channel_command_rules_" + command_rule_set_type + "_rules_desc")

    members = []
    for member_id in command_rule_set.users:
        member = context.message.channel.get_member(member_id)
        member_name = None

        if member is not None:
            member_name = "{member.display_name} ({member.id})".format(member=member)
        else:
            member_name = "[{former_member}] ({id})".format(
                former_member=await context.language.get_text("former_channel_member"),
                id=member_id)

        members.append(member_name)

    roles = []
    for role_id in command_rule_set.roles:
        role = context.message.channel.get_role(role_id)
        role_name = None
        if role is not None:
            role_name = "{role.name} ({role.id})".format(role=role)
        else:
            role_name = "[{former_role}] ({id})".format(
                former_role=await context.language.get_text("former_channel_role"),
                id=role_id)

        roles.append(role_name)

    permissions = []
    if command_rule_set.permissions is not None:
        for permission_code in command_rule_set.permissions:
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


async def display_guild_command_rules(context, arguments):
    """Display one command's command rules for guild."""
    command_rule_object = arguments[0]

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "display_guild_command_rules_title",
            {"command": command_rule_object["name"]}))

    command_rule_set_type = None
    if not command_rule_object["rule"].inclusionary.is_empty:
        command_rule_set_type = "inclusionary"

    elif not command_rule_object["rule"].exclusionary.is_empty:
        command_rule_set_type = "exclusionary"

    else:
        message.embed.description = await context.language.get_text(
            "display_guild_command_rules_no_command_rules")

        await message.send(context)
        return

    command_rule_set = getattr(command_rule_object["rule"], command_rule_set_type)
    message.embed.description = await context.language.get_text(
        "display_guild_command_rules_" + command_rule_set_type + "_rules_desc")

    members = []
    for member_id in command_rule_set.users:
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
    for role_id in command_rule_set.roles:
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
    if command_rule_set.permissions is not None:
        for permission_code in command_rule_set.permissions:
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
