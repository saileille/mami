"""Configuration data classes."""
from bot.data import definitions
from framework import custom_json


class ConfigData():
    """Super-class for UserData, ChannelData, CategoryData and GuildData."""

    def __init__(self,
                 prefix=None,
                 language_id=None,
                 shortcuts=None):
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


class UserData(ConfigData):
    """User data and configuration."""

    def __init__(self,
                 prefix=None,
                 language_id=None,
                 shortcuts=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

    @staticmethod
    def create_object_from_database(row):
        """Create UserData object from a database row."""
        if row is None:
            return None

        return UserData(prefix=row[0], language_id=row[1])


class ChannelData(ConfigData):
    """Channel data and configuration."""

    def __init__(self,
                 prefix=None,
                 language_id=None,
                 shortcuts=None,
                 checks=None,
                 max_dice=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.checks = checks
        self.max_dice = max_dice

        if self.checks is None:
            self.checks = custom_json.load(definitions.EMPTY_DEFAULT_CHECKS)

    async def check_command_rules(self, message, command_id_list):
        """Check command rules by passing it on to Checks object."""
        return await self.checks.check_rules(message, command_id_list)

    @staticmethod
    def create_object_from_database(row):
        """Create ChannelData object from a database row."""
        if row is None:
            return None

        return ChannelData(
            prefix=row[0], language_id=row[1], checks=custom_json.load(row[2]),
            max_dice=row[3])


class CategoryData(ConfigData):
    """Channel data and configuration."""

    def __init__(self,
                 prefix=None,
                 language_id=None,
                 shortcuts=None,
                 checks=None,
                 max_dice=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.checks = checks
        self.max_dice = max_dice

        if self.checks is None:
            self.checks = custom_json.load(definitions.EMPTY_DEFAULT_CHECKS)

    async def check_command_rules(self, message, command_id_list):
        """Check command rules by passing it on to Checks object."""
        return await self.checks.check_rules(message, command_id_list)

    @staticmethod
    def create_object_from_database(row):
        """Create CategoryData object from a database row."""
        if row is None:
            return None

        return CategoryData(
            prefix=row[0], language_id=row[1], checks=custom_json.load(row[2]),
            max_dice=row[3])


class GuildData(ConfigData):
    """Guild data and configuration."""

    def __init__(self,
                 prefix=None,
                 language_id=None,
                 shortcuts=None,
                 checks=None,
                 max_dice=None):
        """Object initialisation."""
        super().__init__(prefix, language_id, shortcuts)

        self.checks = checks
        self.max_dice = max_dice

        if self.checks is None:
            self.checks = custom_json.load(definitions.GUILD_DEFAULT_CHECKS)

    async def check_command_rules(self, message, command_id_list):
        """Check command rules by passing it on to Checks object."""
        allow = await self.checks.check_rules(message, command_id_list)
        if allow is None:
            allow = True

        return allow

    @staticmethod
    def create_object_from_database(row):
        """Create GuildData object from a database row."""
        if row is None:
            return None

        return GuildData(
            prefix=row[0], language_id=row[1], checks=custom_json.load(row[2]),
            max_dice=row[3])
