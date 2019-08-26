"""Anything and everything related to shortcuts."""
import random

from bot.database import database_functions
from bot.data import definitions
from framework import embeds


class Shortcut():
    """The Shortcut class."""

    def __init__(self,
                 name=None,
                 creator=None,
                 content=None):
        """Object initialisation."""
        self.name = name
        self.creator = creator
        self.content = content

    async def get_creator_name(self, context):
        """
        Get the display name of the shortcut creator.

        If the member is no longer part of the guild, return an appropriate text for the
        language.
        """
        member = context.message.guild.get_member(self.creator)

        name = None
        if member is None:
            name = await context.language.get_text("former_guild_member")
            name = "[" + name + "]"
        else:
            name = member.display_name

        return name

    @staticmethod
    async def create_object_from_database(row):
        """Create Shortcut object from a database row."""
        if row is None:
            return None

        return Shortcut(name=row[0], creator=row[1], content=row[2])


async def add_shortcut(context, arguments, platform_type):
    """
    Add a shortcut in the database.

    Parametre "platform_type" is "category", "channel", "guild" or "user".
    """
    shortcut = Shortcut(arguments[0], context.message.author.id, arguments[1])
    data_object = getattr(context, platform_type + "_data")

    data_object.shortcuts[shortcut.name] = shortcut
    await database_functions.insert_shortcut(context, shortcut, platform_type)

    message = embeds.PaginatedEmbed(
        await context.language.get_text(platform_type + "_shortcut_added_title"))

    shortcut_cmd = definitions.COMMANDS.sub_commands["shortcut"]
    shortcut_name = shortcut.name
    if " " in shortcut_name:
        shortcut_name = '"' + shortcut_name + '"'

    shortcut_call = "{shortcut_cmd} {shortcut_name}".format(
        shortcut_cmd=await shortcut_cmd.get_command_string(context),
        shortcut_name=shortcut_name)

    message.embed.description = "✅ " + await context.language.get_text(
        platform_type + "_shortcut_added_desc",
        {"shortcut": shortcut.name, "shortcut_call": shortcut_call})

    await message.send(context)
    return True


async def add_category_shortcut(context, arguments):
    """Add a category shortcut in the database."""
    return await add_shortcut(context, arguments, "category")


async def add_channel_shortcut(context, arguments):
    """Add a channel shortcut in the database."""
    return await add_shortcut(context, arguments, "channel")


async def add_guild_shortcut(context, arguments):
    """Add a guild shortcut in the database."""
    return await add_shortcut(context, arguments, "guild")


async def add_user_shortcut(context, arguments):
    """Add a user shortcut in the database."""
    return await add_shortcut(context, arguments, "user")


async def delete_shortcut(context, arguments, platform_type):
    """Delete a shortcut from the database."""
    shortcut_name = arguments[0]
    data_object = getattr(context, platform_type + "_data")

    await database_functions.delete_shortcut(context, shortcut_name, platform_type)
    del data_object.shortcuts[shortcut_name]

    message = embeds.PaginatedEmbed(
        await context.language.get_text(platform_type + "_shortcut_deleted_title"))

    message.embed.description = "✅ " + await context.language.get_text(
        platform_type + "_shortcut_deleted_desc", {"shortcut": shortcut_name})

    await message.send(context)
    return True


async def delete_category_shortcut(context, arguments):
    """Delete a category shortcut from the database."""
    return await delete_shortcut(context, arguments, "category")


async def delete_channel_shortcut(context, arguments):
    """Delete a channel shortcut from the database."""
    return await delete_shortcut(context, arguments, "channel")


async def delete_guild_shortcut(context, arguments):
    """Delete a guild shortcut from the database."""
    return await delete_shortcut(context, arguments, "guild")


async def delete_user_shortcut(context, arguments):
    """Delete a user shortcut from the database."""
    return await delete_shortcut(context, arguments, "user")


async def display_shortcuts(context, platform_type):
    """Display all platform shortcuts."""
    shortcuts = []
    data_object = getattr(context, platform_type + "_data")
    for shortcut in data_object.shortcuts.values():
        shortcuts.append(shortcut.name)

    shortcuts.sort()

    shortcut_command = definitions.COMMANDS.get_sub_command_from_path("shortcut")
    shortcut_cmd_name = await shortcut_command.get_command_string(context)

    shortcut_instruction = shortcut_cmd_name + " [" + (
        await context.language.get_text("display_shortcuts_shortcut_name")) + "]"

    random_shortcut = random.choice(shortcuts)
    if " " in random_shortcut:
        random_shortcut = '"' + random_shortcut + '"'

    shortcut_example = shortcut_cmd_name + " " + random_shortcut

    message = embeds.PaginatedEmbed(
        await context.language.get_text("display_" + platform_type + "_shortcuts_title"),
        embeds.EmbedFieldCollection(
            shortcuts, await context.language.get_text("display_shortcuts_subtitle"), 2))

    message.embed.description = await context.language.get_text(
        "display_" + platform_type + "_shortcuts_desc",
        {"instruction": shortcut_instruction, "example": shortcut_example})

    await message.send(context)
    return True


async def display_category_shortcuts(context, arguments):
    """Display all category shortcuts."""
    return await display_shortcuts(context, "category")


async def display_channel_shortcuts(context, arguments):
    """Display all channel shortcuts."""
    return await display_shortcuts(context, "channel")


async def display_guild_shortcuts(context, arguments):
    """Display all guild shortcuts."""
    return await display_shortcuts(context, "guild")


async def display_user_shortcuts(context, arguments):
    """Display all user shortcuts."""
    return await display_shortcuts(context, "user")


async def use_shortcut(context, arguments):
    """Use a shortcut."""
    await context.message.channel.send(arguments[0].content)
    return True
