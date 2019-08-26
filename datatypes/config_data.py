"""Configuration data classes."""
from bot.data import definitions
from bot.mechanics.guild_call import GuildCall
from framework import custom_json


class ConfigData():
    """Super-class for UserData, ChannelData, CategoryData and GuildData."""

    def __init__(self, prefix=None, language_id=None, shortcuts=None):
        """Object initialisation."""
        self.prefix = prefix
        self.language_id = language_id
        self.shortcuts = shortcuts

        if self.shortcuts is None:
            self.shortcuts = {}

        self._language = None

    @property
    def language(self):
        """Get language object from ID."""
        if self._language is None and self.language_id is not None:
            self._language = definitions.LANGUAGES[self.language_id]

        return self._language

    async def clear_cache(self):
        """Clear the cache."""
        self._language = None


class CategoryData(ConfigData):
    """Category data and configuration."""

    def __init__(
            self, prefix=None, language_id=None, shortcuts=None, command_data=None,
            max_dice=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.command_data = command_data
        self.max_dice = max_dice

        if self.command_data is None:
            self.command_data = custom_json.load(definitions.DEFAULT_COMMAND_DATA)

    async def check_command_rules(self, message, command_id_list):
        """Check command rules by passing it on to CommandData object."""
        return await self.command_data.check_rules(message, command_id_list)

    @staticmethod
    def create_object_from_database(row):
        """Create CategoryData object from a database row."""
        if row is None:
            return None

        return CategoryData(
            prefix=row[0], language_id=row[1], command_data=custom_json.load(row[2]),
            max_dice=row[3])


class ChannelData(ConfigData):
    """Channel data and configuration."""

    def __init__(
            self, prefix=None, language_id=None, shortcuts=None, command_data=None,
            max_dice=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.command_data = command_data
        self.max_dice = max_dice
        self.guild_call = GuildCall(None, False)

        if self.command_data is None:
            self.command_data = custom_json.load(definitions.DEFAULT_COMMAND_DATA)

    async def check_command_rules(self, message, command_id_list):
        """Check command rules by passing it on to CommandData object."""
        return await self.command_data.check_rules(message, command_id_list)

    @staticmethod
    def create_object_from_database(row):
        """Create ChannelData object from a database row."""
        if row is None:
            return None

        return ChannelData(
            prefix=row[0], language_id=row[1], command_data=custom_json.load(row[2]),
            max_dice=row[3])


class GuildData(ConfigData):
    """Guild data and configuration."""

    def __init__(
            self, prefix=None, language_id=None, shortcuts=None, command_data=None,
            max_dice=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.command_data = command_data
        self.max_dice = max_dice

        if self.command_data is None:
            self.command_data = custom_json.load(definitions.GUILD_COMMAND_DATA)

    async def check_command_rules(self, message, command_id_list):
        """Check command rules by passing it on to CommandData object."""
        allow_use = await self.command_data.check_rules(message, command_id_list)
        if allow_use is None:
            allow_use = True

        return allow_use

    @staticmethod
    def create_object_from_database(row):
        """Create GuildData object from a database row."""
        if row is None:
            return None

        return GuildData(
            prefix=row[0], language_id=row[1], command_data=custom_json.load(row[2]),
            max_dice=row[3])


class UserData(ConfigData):
    """User data and configuration."""

    def __init__(self, prefix=None, language_id=None, shortcuts=None, command_data=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.command_data = command_data
        if self.command_data is None:
            self.command_data = custom_json.load(definitions.USER_COMMAND_DATA)

    @staticmethod
    def create_object_from_database(row):
        """Create UserData object from a database row."""
        if row is None:
            return None

        return UserData(
            prefix=row[0], language_id=row[1], command_data=custom_json.load(row[2]))


class GlobalData():
    """For collecting statistics and such from the bot."""

    def __init__(self, command_data=None):
        """Initialise object."""
        self.command_data = command_data

        if self.command_data is None:
            self.command_data = custom_json.load(definitions.USER_COMMAND_DATA)

    @staticmethod
    async def create_object_from_database(row):
        """Create GlobalData object from a database row."""
        command_data = None
        if row is not None:
            command_data = custom_json.load(row[0])

        return GlobalData(command_data=command_data)
