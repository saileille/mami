"""Bot database stuff."""
import os
import sqlite3

from bot.commands import shortcuts
from bot.data import definitions
from datatypes import config_data
from framework import custom_json


PLURAL = {
    "category": "categories", "channel": "channels", "guild": "guilds", "user": "users"}


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
        CREATE TABLE IF NOT EXISTS "users"(
            id INTEGER NOT NULL,
            prefix TEXT,
            language TEXT,
            command_data TEXT,
            PRIMARY KEY("id")
        );
    """
    channel_table = """
        CREATE TABLE IF NOT EXISTS "channels"(
            id INTEGER NOT NULL,
            prefix TEXT,
            language TEXT,
            command_data TEXT,
            max_dice INTEGER,
            PRIMARY KEY("id")
        );
    """
    category_table = """
        CREATE TABLE IF NOT EXISTS "categories"(
            id INTEGER NOT NULL,
            prefix TEXT,
            language TEXT,
            command_data TEXT,
            max_dice INTEGER,
            PRIMARY KEY("id")
        );
    """
    guild_table = """
        CREATE TABLE IF NOT EXISTS "guilds"(
            id INTEGER NOT NULL,
            prefix TEXT,
            language TEXT,
            command_data TEXT,
            max_dice INTEGER,
            PRIMARY KEY("id")
        );
    """
    shortcut_table = """
        CREATE TABLE IF NOT EXISTS "shortcuts"(
            name TEXT NOT NULL,
            platform_id INTEGER NOT NULL,
            platform_type TEXT NOT NULL,
            creator INTEGER,
            content TEXT,
            PRIMARY KEY("name", "platform_id", "platform_type")
        );
    """
    global_table = """
        CREATE TABLE IF NOT EXISTS "global"(
            command_data TEXT NOT NULL,
            PRIMARY KEY("command_data")
        );
    """

    definitions.DATABASE_CURSOR.execute(user_table)
    definitions.DATABASE_CURSOR.execute(channel_table)
    definitions.DATABASE_CURSOR.execute(category_table)
    definitions.DATABASE_CURSOR.execute(guild_table)
    definitions.DATABASE_CURSOR.execute(shortcut_table)
    definitions.DATABASE_CURSOR.execute(global_table)
    definitions.DATABASE_CONNECTION.commit()


def update_database():
    """
    Update the database before launching Mami.

    Update the database if necessary, and only if necessary.
    Clear this function of code after one use.
    """


async def insert_global_data():
    """Insert the global data."""
    statement = """
        INSERT INTO global(command_data)
        VALUES(?)
    """

    variables = (definitions.USER_COMMAND_DATA,)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_user(obj_id):
    """Insert default user. Used when there is no previous record."""
    statement = """
        INSERT INTO users(id, prefix, language, command_data)
        VALUES(?, NULL, NULL, ?)
    """

    variables = (obj_id, definitions.USER_COMMAND_DATA)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_channel(obj_id):
    """Insert default channel. Used when there is no previous record."""
    statement = """
        INSERT INTO channels(id, prefix, language, command_data, max_dice)
        VALUES(?, NULL, NULL, ?, NULL)
    """

    variables = (obj_id, definitions.DEFAULT_COMMAND_DATA)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_category(obj_id):
    """Insert default category. Used when there is no previous record."""
    statement = """
        INSERT INTO categories(id, prefix, language, command_data, max_dice)
        VALUES(?, NULL, NULL, ?, NULL)
    """

    variables = (obj_id, definitions.DEFAULT_COMMAND_DATA)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_guild(obj_id):
    """Insert default guild. Used when there is no previous record."""
    statement = """
        INSERT INTO guilds(id, prefix, language, command_data, max_dice)
        VALUES(?, NULL, NULL, ?, NULL)
    """

    variables = (obj_id, definitions.GUILD_COMMAND_DATA)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def insert_shortcut(context, shortcut, platform_type):
    """Insert a new shortcut into the database."""
    statement = """
        INSERT INTO shortcuts(name, platform_id, platform_type, creator, content)
        VALUES(?, ?, ?, ?, ?)
    """

    platform_id = await get_id_from_platform(context.message, platform_type)
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

    platform_id = await get_id_from_platform(context.message, platform_type)
    variables = (name, platform_id, platform_type)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


def select_all_channels():
    """
    Select all channels in the database.

    Synchronous method. Used when starting up Mami.
    """
    statement = """
        SELECT id, prefix, language, command_data, max_dice
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
        SELECT id, prefix, language, command_data, max_dice
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
        SELECT id, prefix, language, command_data, max_dice
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
        SELECT id, prefix, language, command_data
        FROM users
    """

    definitions.DATABASE_CURSOR.execute(statement)
    data = definitions.DATABASE_CURSOR.fetchall()

    users = {}
    for row in data:
        users[row[0]] = config_data.UserData.create_object_from_database(row[1:])

    return users


async def select_global_data():
    """Select the global data."""
    statement = """
        SELECT command_data FROM global
    """

    definitions.DATABASE_CURSOR.execute(statement)
    row = definitions.DATABASE_CURSOR.fetchone()
    if row is None:
        await insert_global_data()

    return await config_data.GlobalData.create_object_from_database(row)


async def select_channel(obj_id):
    """Select channel based on the ID."""
    statement = """
        SELECT prefix, language, command_data, max_dice
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
        SELECT prefix, language, command_data, max_dice
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
        SELECT prefix, language, command_data, max_dice
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
        SELECT prefix, language, command_data
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
            language = ?,
            command_data = ?
        WHERE id = ?
    """

    variables = (
        context.user_data.prefix, context.user_data.language_id,
        custom_json.save(context.user_data.command_data),
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
        custom_json.save(context.channel_data.command_data),
        context.channel_data.max_dice, context.message.channel.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_category(context):
    """Update the category."""
    statement = """
        UPDATE categories SET
            prefix = ?,
            language = ?,
            command_data = ?,
            max_dice = ?
        WHERE id = ?
    """

    variables = (
        context.category_data.prefix, context.category_data.language_id,
        custom_json.save(context.category_data.command_data),
        context.category_data.max_dice, context.message.channel.category_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_guild(context):
    """Update the guild."""
    statement = """
        UPDATE guilds SET
            prefix = ?,
            language = ?,
            command_data = ?,
            max_dice = ?
        WHERE id = ?
    """

    variables = (
        context.guild_data.prefix, context.guild_data.language_id,
        custom_json.save(context.guild_data.command_data), context.guild_data.max_dice,
        context.message.guild.id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_language(context, platform):
    """Update language to the database."""
    statement = """
        UPDATE {table} SET
            language = ?
        WHERE id = ?
    """.format(table=PLURAL[platform])

    platform_data = getattr(context, platform + "_data")
    platform_id = await get_id_from_platform(context.message, platform)

    variables = (platform_data.language_id, platform_id)
    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_command_data(context, platform):
    """Update command data for selected platform."""
    statement = """
        UPDATE {table} SET
            command_data = ?
        WHERE id = ?
    """.format(table=PLURAL[platform])

    platform_data = getattr(context, platform + "_data")
    platform_id = await get_id_from_platform(context.message, platform)

    variables = (custom_json.save(platform_data.command_data), platform_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def update_global_command_data(context):
    """Update command data for global data."""
    statement = """
        UPDATE global SET
            command_data = ?
    """
    variables = (custom_json.save(context.global_data.command_data),)

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
            command_data = ?
        WHERE id = ?
    """

    variables = (
        category.language_id, custom_json.save(category.command_data), category_id)

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
            command_data = ?
        WHERE id = ?
    """

    variables = (channel.language_id, custom_json.save(channel.command_data), channel_id)

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
            command_data = ?
        WHERE id = ?
    """

    variables = (guild.language_id, custom_json.save(guild.command_data), guild_id)

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
            language = ?,
            command_data = ?
        WHERE id = ?
    """

    variables = (user.language_id, custom_json.save(user.command_data), user_id)

    definitions.DATABASE_CURSOR.execute(statement, variables)
    definitions.DATABASE_CONNECTION.commit()


async def get_id_from_platform(message, platform):
    """Get the appropriate ID of the platform."""
    platform_id = None
    if platform == "user":
        platform_id = message.author.id
    elif platform == "channel":
        platform_id = message.channel.id
    elif platform == "category":
        platform_id = message.channel.category_id
    elif platform == "guild":
        platform_id = message.guild.id

    return platform_id
