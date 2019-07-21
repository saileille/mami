"""Conversions of users and roles."""
import re
from bot.misc import embed_messages


async def id_to_member(argument, context):
    """
    Check if the argument is a valid member mention or ID.

    If valid, return the Member object.
    """
    user_mention = r"<@!?([0-9]{18})>"
    match = re.fullmatch(user_mention, argument)

    user_id = None
    if match is None:
        try:
            user_id = int(argument)
        except ValueError:
            return None
    else:
        user_id = int(match.group(1))

    member = context.message.guild.get_member(user_id)
    return member


async def id_to_role(argument, context):
    """
    Check if the argument is a valid role mention or ID.

    If valid, return the Role object.
    """
    role_mention = r"<@&([0-9]{18})>"
    match = re.fullmatch(role_mention, argument)

    role_id = None
    if match is None:
        try:
            role_id = int(argument)
        except ValueError:
            return None
    else:
        role_id = int(match.group(1))

    for role in context.message.guild.roles:
        if role_id == role.id:
            return role

    return None


async def name_to_member(argument, context):
    """
    Check if the argument is a valid member name.

    Username, username + discriminator and nickname are all accepted.

    If valid, return the Member object.
    """
    return context.message.guild.get_member_named(argument)


async def name_to_role(argument, context):
    """
    Check if the argument is a valid role name.

    If valid, return the Role object.
    """
    for role in context.message.guild.roles:
        if argument == role.name:
            return role

    return None


async def name_to_permission(argument, context):
    """
    Check if argument is a valid permission name.

    If valid, return the permission code.
    """
    for key in context.language.permission_names:
        permission = context.language.permission_names[key]
        if argument == permission:
            return key

    return None


async def member_role_permission(argument, context):
    """
    Check if the argument is a valid member, role or permission.

    If valid, return the Member or Role object, or permission code.
    """
    convert_functions = [
        name_to_permission, id_to_role, id_to_member, name_to_role, name_to_member]

    conversion = None
    for function in convert_functions:
        conversion = await function(argument, context)
        if conversion is not None:
            return conversion

    custom_msg = await context.language.get_text("not_member_role_or_permission")
    await embed_messages.invalid_argument(context, argument, custom_msg)
    return conversion


async def valid_member(argument, context):
    """
    Check if the argument is a valid guild member.

    If valid, return the Member object.
    """
    convert_functions = [id_to_member, name_to_member]

    conversion = None
    for function in convert_functions:
        conversion = await function(argument, context)
        if conversion is not None:
            return conversion

    custom_msg = await context.language.get_text("not_member")
    await embed_messages.invalid_argument(context, argument, custom_msg)
    return conversion
