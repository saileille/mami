"""Bot database stuff."""
import json
import os
import sqlite3

from bot.commands import shortcuts
from bot.data import definitions
from datatypes import config_data
from framework import custom_json


def connect():
    """Set up and connect to database."""
    path = os.path.join(definitions.ROOT_DIR, "bot\\database\\database.db")

    definitions.DATABASE_CONNECTION = sqlite3.connect(path)
    definitions.DATABASE_CURSOR = definitions.DATABASE_CONNECTION.cursor()

    create_tables()
    update_database()


def create_tables():
    """Create the necessary tables if they do not exist already."""
    user_table = """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            prefix TEXT,
            language TEXT
        );
    """
    channel_table = """
        CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY,
            prefix TEXT,
            language TEXT,
            checks TEXT,
            max_dice INTEGER
        );
    """
    category_table = """
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY,
            prefix TEXT,
            language TEXT,
            checks TEXT,
            max_dice INTEGER
        );
    """
    guild_table = """
        CREATE TABLE IF NOT EXISTS guilds(
            id INTEGER PRIMARY KEY,
            prefix TEXT,
            language TEXT,
            checks TEXT,
            max_dice INTEGER
        );
    """
    shortcut_table = """
        CREATE TABLE IF NOT EXISTS shortcuts(
            name TEXT,
            platform_id INTEGER,
            platform_type TEXT,
            creator INTEGER,
            content TEXT,
            PRIMARY KEY(name, platform_id, platform_type)
        );
    """

    definitions.DATABASE_CURSOR.execute(user_table)
    definitions.DATABASE_CURSOR.execute(channel_table)
    definitions.DATABASE_CURSOR.execute(category_table)
    definitions.DATABASE_CURSOR.execute(guild_table)
    definitions.DATABASE_CURSOR.execute(shortcut_table)
    definitions.DATABASE_CONNECTION.commit()


def update_database():
    """
    Update the database before launching Mami.

    Update the database if necessary, and only if necessary.
    Clear this function of code after one use.
    """


async def insert_user(obj_id):
    """Insert default user. Used when there is no previous record."""
    statement = """
        INSERT INTO users(id, prefix, language)
        VALUES(?, NULL, NULL)
    """

    variables = (obj_id,)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_channel(obj_id):
    """Insert default channel. Used when there is no previous record."""
    statement = """
        INSERT INTO channels(id, prefix, language, checks, max_dice)
        VALUES(?, NULL, NULL, ?, NULL)
    """

    variables = (obj_id, definitions.EMPTY_COMMAND_RULES)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_category(obj_id):
    """Insert default category. Used when there is no previous record."""
    statement = """
        INSERT INTO categories(id, prefix, language, checks, max_dice)
        VALUES(?, NULL, NULL, ?, NULL)
    """

    variables = (obj_id, definitions.EMPTY_COMMAND_RULES)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_guild(obj_id):
    """Insert default guild. Used when there is no previous record."""
    statement = """
        INSERT INTO guilds(id, prefix, language, checks, max_dice)
        VALUES(?, NULL, NULL, ?, NULL)
    """

    variables = (obj_id, definitions.GUILD_DEFAULT_COMMAND_RULES)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_shortcut(context, shortcut, platform_type):
    """Insert a new shortcut into the database."""
    statement = """
        INSERT INTO shortcuts(name, platform_id, platform_type, creator, content)
        VALUES(?, ?, ?, ?, ?)
    """

    platform_id = None
    if platform_type == "user":
        platform_id = context.message.author.id
    elif platform_type == "channel":
        platform_id = context.message.channel.id
    elif platform_type == "category":
        platform_id = context.message.channel.category_id
    elif platform_type == "guild":
        platform_id = context.message.guild.id

    variables = (shortcut.name, platform_id, platform_type, shortcut.creator,
                 shortcut.content)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def delete_shortcut(context, name, platform_type):
    """Remove a shortcut from the database."""
    statement = """
        DELETE FROM shortcuts
        WHERE name = ? AND platform_id = ? AND platform_type = ?
    """

    platform_id = None
    if platform_type == "user":
        platform_id = context.message.author.id
    elif platform_type == "channel":
        platform_id = context.message.channel.id
    elif platform_type == "category":
        platform_id = context.message.channel.category_id
    elif platform_type == "guild":
        platform_id = context.message.guild.id

    variables = (name, platform_id, platform_type)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


def select_all_channels():
    """
    Select all channels in the database.

    Synchronous method. Used when starting up Mami.
    """
    statement = """
        SELECT id, prefix, language, checks, max_dice
        FROM channels
    """

    definitions.DATABASE_CURSOR.execute(statement)
    data = definitions.DATABASE_CURSOR.fetchall()

    channels = {}
    for row in data:
        channels[row[0]] = config_data.ChannelData.create_object_from_database(row[1:])

    return channels


def select_all_categories():
    """
    Select all categories in the database.

    Synchronous method. Used when starting up Mami.
    """
    statement = """
        SELECT id, prefix, language, checks, max_dice
        FROM categories
    """

    definitions.DATABASE_CURSOR.execute(statement)
    data = definitions.DATABASE_CURSOR.fetchall()

    categories = {}
    for row in data:
        categories[row[0]] = config_data.CategoryData.create_object_from_database(row[1:])

    return categories


def select_all_guilds():
    """
    Select all guilds in the database.

    Synchronous method. Used when starting up Mami.
    """
    statement = """
        SELECT id, prefix, language, checks, max_dice
        FROM guilds
    """

    definitions.DATABASE_CURSOR.execute(statement)
    data = definitions.DATABASE_CURSOR.fetchall()

    guilds = {}
    for row in data:
        guilds[row[0]] = config_data.GuildData.create_object_from_database(row[1:])

    return guilds


def select_all_users():
    """
    Select all users in the database.

    Synchronous method. Used when starting up Mami.
    """
    statement = """
        SELECT id, prefix, language
        FROM users
    """

    definitions.DATABASE_CURSOR.execute(statement)
    data = definitions.DATABASE_CURSOR.fetchall()

    users = {}
    for row in data:
        users[row[0]] = config_data.UserData.create_object_from_database(row[1:])

    return users


async def select_channel(obj_id):
    """Select channel based on the ID."""
    statement = """
        SELECT prefix, language, checks, max_dice
        FROM channels
        WHERE id = ?
    """

    variables = (obj_id,)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    row = definitions.DATABASE_CURSOR.fetchone()
    channel = config_data.ChannelData.create_object_from_database(row)

    await select_shortcuts(channel, obj_id, "channel")
    return channel


async def select_category(obj_id):
    """Select category based on the ID."""
    statement = """
        SELECT prefix, language, checks, max_dice
        FROM categories
        WHERE id = ?
    """

    variables = (obj_id,)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    row = definitions.DATABASE_CURSOR.fetchone()
    category = config_data.CategoryData.create_object_from_database(row)

    await select_shortcuts(category, obj_id, "category")
    return category


async def select_guild(obj_id):
    """Select guild based on the ID."""
    statement = """
        SELECT prefix, language, checks, max_dice
        FROM guilds
        WHERE id = ?
    """

    variables = (obj_id,)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    row = definitions.DATABASE_CURSOR.fetchone()
    guild = config_data.GuildData.create_object_from_database(row)

    await select_shortcuts(guild, obj_id, "guild")
    return guild


async def select_user(obj_id):
    """Select user based on the ID."""
    statement = """
        SELECT prefix, language
        FROM users
        WHERE id = ?
    """

    variables = (obj_id,)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    row = definitions.DATABASE_CURSOR.fetchone()
    user = config_data.UserData.create_object_from_database(row)

    await select_shortcuts(user, obj_id, "user")
    return user


async def select_shortcuts(obj, obj_id, platform_type=None):
    """Select user, channel or guild-specific shortcuts."""
    statement = """
        SELECT name, creator, content
        FROM shortcuts
        WHERE platform_id = ? AND platform_type = ?
    """

    if platform_type is None:
        if isinstance(obj, config_data.UserData):
            platform_type = "user"
        elif isinstance(obj, config_data.ChannelData):
            platform_type = "channel"
        elif isinstance(obj, config_data.GuildData):
            platform_type = "guild"

    variables = (obj_id, platform_type)
    definitions.DATABASE_CURSOR.execute(statement, variables)

    shortcut_rows = definitions.DATABASE_CURSOR.fetchall()
    for row in shortcut_rows:
        shortcut = await shortcuts.Shortcut.create_object_from_database(row)
        obj.shortcuts[shortcut.name] = shortcut


async def update_user(context):
    """Update the user."""
    statement = """
        UPDATE users SET
            prefix = ?,
            language = ?
        WHERE id = ?
    """

    variables = (context.user_data.prefix,
                 context.user_data.language_id,
                 context.message.author.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_channel(context):
    """Update the channel."""
    statement = """
        UPDATE channels SET
            prefix = ?,
            language = ?,
            checks = ?,
            max_dice = ?
        WHERE id = ?
    """

    variables = (
        context.channel_data.prefix, context.channel_data.language_id,
        custom_json.save(context.channel_data.command_rules),
        context.channel_data.max_dice, context.message.channel.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_category(context):
    """Update the category."""
    statement = """
        UPDATE categories SET
            prefix = ?,
            language = ?,
            checks = ?,
            max_dice = ?
        WHERE id = ?
    """

    variables = (
        context.category_data.prefix, context.category_data.language_id,
        custom_json.save(context.category_data.command_rules),
        context.category_data.max_dice, context.message.channel.category_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_guild(context):
    """Update the guild."""
    statement = """
        UPDATE guilds SET
            prefix = ?,
            language = ?,
            checks = ?,
            max_dice = ?
        WHERE id = ?
    """

    variables = (
        context.guild_data.prefix, context.guild_data.language_id,
        custom_json.save(context.guild_data.command_rules), context.guild_data.max_dice,
        context.message.guild.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_category_language(context):
    """Update the category language to the database."""
    statement = """
        UPDATE categories SET
            language = ?
        WHERE id = ?
    """

    variables = (context.category_data.language_id, context.message.channel.category_id)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_channel_language(context):
    """Update the channel language to the database."""
    statement = """
        UPDATE channels SET
            language = ?
        WHERE id = ?
    """

    variables = (context.channel_data.language_id, context.message.channel.category_id)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_guild_language(context):
    """Update the guild language to the database."""
    statement = """
        UPDATE guilds SET
            language = ?
        WHERE id = ?
    """

    variables = (context.guild_data.language_id, context.message.guild.id)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_user_language(context):
    """Update the user language to the database."""
    statement = """
        UPDATE users SET
            language = ?
        WHERE id = ?
    """

    variables = (context.user_data.language_id, context.message.guild.id)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_category_command_rules(context):
    """Update the category command rules to the database."""
    statement = """
        UPDATE categories SET
            checks = ?
        WHERE id = ?
    """

    variables = (
        custom_json.save(context.category_data.command_rules),
        context.message.category.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_channel_command_rules(context):
    """Update the channel command rules to the database."""
    statement = """
        UPDATE channels SET
            checks = ?
        WHERE id = ?
    """

    variables = (
        custom_json.save(context.channel_data.command_rules), context.message.channel.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_guild_command_rules(context):
    """Update the guild command rules to the database."""
    statement = """
        UPDATE guilds SET
            checks = ?
        WHERE id = ?
    """

    variables = (
        custom_json.save(context.guild_data.command_rules), context.message.guild.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


def synchronise_category_update(category_id, category):
    """
    Update the category when synchronising data.

    Update the relevant category data at startup when making sure there are no
    compatibility issues with the data stored and the current Mami version.
    """
    statement = """
        UPDATE categories SET
            language = ?,
            checks = ?
        WHERE id = ?
    """

    variables = (
        category.language_id, custom_json.save(category.command_rules), category_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


def synchronise_channel_update(channel_id, channel):
    """
    Update the channel when synchronising data.

    Update the relevant channel data at startup when making sure there are no
    compatibility issues with the data stored and the current Mami version.
    """
    statement = """
        UPDATE channels SET
            language = ?,
            checks = ?
        WHERE id = ?
    """

    variables = (channel.language_id, custom_json.save(channel.command_rules), channel_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


def synchronise_guild_update(guild_id, guild):
    """
    Update the guild when synchronising data.

    Update the relevant guild data at startup when making sure there are no compatibility
    issues with the data stored and the current Mami version.
    """
    statement = """
        UPDATE guilds SET
            language = ?,
            checks = ?
        WHERE id = ?
    """

    variables = (guild.language_id, custom_json.save(guild.command_rules), guild_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


def synchronise_user_update(user_id, user):
    """
    Update the user when synchronising data.

    Update the relevant user data at startup when making sure there are no compatibility
    issues with the data stored and the current Mami version.
    """
    statement = """
        UPDATE users SET
            language = ?
        WHERE id = ?
    """

    variables = (user.language_id, user_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()
