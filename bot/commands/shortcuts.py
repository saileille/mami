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


async def add_guild_shortcut(context, command_input):
    """Add a guild shortcut in the database."""
    shortcut = Shortcut(
        command_input.arguments[0], context.message.author.id, command_input.arguments[1])

    context.guild_data.shortcuts[shortcut.name] = shortcut
    await database_functions.insert_shortcut(context, shortcut, "guild")

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_shortcut_added_title"))

    shortcut_cmd = definitions.COMMANDS.sub_commands["shortcut"]
    shortcut_call = await shortcut_cmd.get_command_string(context)

    shortcut_name = shortcut.name
    if " " in shortcut_name:
        shortcut_name = '"' + shortcut_name + '"'

    shortcut_call += " " + shortcut_name

    message.embed.description = ":white_check_mark: " + await context.language.get_text(
        "guild_shortcut_added_desc",
        {"shortcut": shortcut.name, "shortcut_call": shortcut_call})

    await message.send(context)


async def delete_guild_shortcut(context, command_input):
    """Delete any guild shortcut from the database."""
    shortcut_name = command_input.arguments[0]

    await database_functions.delete_shortcut(context, shortcut_name, "guild")
    del context.guild_data.shortcuts[shortcut_name]

    message = embeds.PaginatedEmbed(
        await context.language.get_text("guild_shortcut_deleted_title"))

    message.embed.description = ":white_check_mark: " + await context.language.get_text(
        "guild_shortcut_deleted_desc", {"shortcut": shortcut_name})

    await message.send(context)


async def display_guild_shortcuts(context, command_input):
    """Display all guild shortcuts."""
    shortcuts = []
    for shortcut in context.guild_data.shortcuts.values():
        shortcuts.append(shortcut.name)

    shortcuts.sort()

    shortcut_command = await definitions.COMMANDS.get_sub_command_from_path(["shortcut"])
    shortcut_cmd_name = await shortcut_command.get_command_string(context)

    shortcut_instruction = shortcut_cmd_name + " [" + (
        await context.language.get_text("display_shortcuts_shortcut_name")) + "]"

    random_shortcut = random.choice(shortcuts)
    if " " in random_shortcut:
        random_shortcut = '"' + random_shortcut + '"'

    shortcut_example = shortcut_cmd_name + " " + random_shortcut

    message = embeds.PaginatedEmbed(
        await context.language.get_text("display_guild_shortcuts_title"),
        embeds.EmbedFieldCollection(
            shortcuts, await context.language.get_text("display_shortcuts_subtitle"), 2))

    message.embed.description = await context.language.get_text(
        "display_guild_shortcuts_desc",
        {"instruction": shortcut_instruction, "example": shortcut_example})

    await message.send(context)


async def use_shortcut(context, command_input):
    """Use a shortcut."""
    await context.message.channel.send(command_input.arguments[0].content)
