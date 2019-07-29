"""Import stuff."""
from bot.database import database_functions
from bot.data import default_values
from bot.data import definitions
from datatypes import config_data


class Context():
    """Contains configuration data and the message."""

    def __init__(self, message):
        """Initialise object."""
        self.message = message
        self.user_data = None
        self.channel_data = None
        self.category_data = None
        self.guild_data = None
        self.ping = None

        self._desktop_ui = None
        self._prefix = None
        self._language_id = None
        self._language = None
        self._max_dice = None

    @property
    def desktop_ui(self):
        """Check what embed layout should be used."""
        if self._desktop_ui is None:
            status = None
            desktop_status = None
            web_status = None
            if self.message.guild is not None:
                status = self.message.author.status
                desktop_status = self.message.author.desktop_status
                web_status = self.message.author.web_status
            else:
                for guild in definitions.CLIENT.guilds:
                    member = guild.get_member(self.message.author.id)
                    if member is not None:
                        status = member.status
                        desktop_status = member.desktop_status
                        web_status = member.web_status
                        break
                else:
                    self._desktop_ui = True
                    return self._desktop_ui

            self._desktop_ui = (
                status.offline or not desktop_status.offline or not web_status.offline)

        return self._desktop_ui

    def check_cached_value(self, attribute_name, default_value):
        """Determine which prefix, language, etc. is used."""
        if getattr(self, "_" + attribute_name) is None:
            check_order = ["user", "channel", "category", "guild"]
            for name in check_order:
                attribute = None
                try:
                    attribute = getattr(getattr(self, name + "_data"), attribute_name)
                except AttributeError:
                    continue

                if attribute is not None:
                    setattr(self, "_" + attribute_name, attribute)
                    return attribute

            setattr(self, "_" + attribute_name, default_value)

        return getattr(self, "_" + attribute_name)

    @property
    def prefix(self):
        """Get the command prefix."""
        return self.check_cached_value("prefix", default_values.PREFIX)

    @property
    def language_id(self):
        """Get the language ID."""
        return self.check_cached_value("language_id", default_values.LANGUAGE_ID)

    @property
    def language(self):
        """Get the language object."""
        if self._language is None:
            self._language = definitions.LANGUAGES[self.language_id]

        return self._language

    @property
    def max_dice(self):
        """Get the maximum amount of dice one can use."""
        return self.check_cached_value("max_dice", default_values.MAX_DICE)

    async def check_command_rules(self, command_id_list):
        """
        Check the command rules.

        Returns whether the command is allowed or not, and a
        list of the IDs leading to the last allowed command.
        """
        check_functions = [
            self.channel_data.check_command_rules, self.guild_data.check_command_rules]

        if self.category_data is not None:
            check_functions.insert(1, self.category_data.check_command_rules)

        allow_use = None
        for function in check_functions:
            allow_use = await function(self.message, command_id_list)
            if allow_use is not None:
                break

        return allow_use

    async def get_category_data(self):
        """
        Get the category data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["categories"]
        if self.message.channel.category_id in cache:
            self.category_data = cache[self.message.channel.category_id]
        else:
            self.category_data = await database_functions.select_category(
                self.message.channel.category_id)

            if self.category_data is None:
                await database_functions.insert_category(self.message.channel.category_id)
                self.category_data = config_data.CategoryData()

            cache[self.message.channel.category_id] = self.category_data

    async def get_channel_data(self):
        """
        Get the channel data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["channels"]
        if self.message.channel.id in cache:
            self.channel_data = cache[self.message.channel.id]
        else:
            self.channel_data = await database_functions.select_channel(
                self.message.channel.id)

            if self.channel_data is None:
                await database_functions.insert_channel(self.message.channel.id)
                self.channel_data = config_data.ChannelData()

            cache[self.message.channel.id] = self.channel_data

    async def get_guild_data(self):
        """
        Get the guild data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["guilds"]
        if self.message.guild.id in cache:
            self.guild_data = cache[self.message.guild.id]
        else:
            self.guild_data = await database_functions.select_guild(
                self.message.guild.id)

            if self.guild_data is None:
                await database_functions.insert_guild(self.message.guild.id)
                self.guild_data = config_data.GuildData()

            cache[self.message.guild.id] = self.guild_data

    async def get_user_data(self):
        """
        Get the user data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["users"]
        if self.message.author.id in cache:
            self.user_data = cache[self.message.author.id]
        else:
            self.user_data = await database_functions.select_user(self.message.author.id)

            if self.user_data is None:
                await database_functions.insert_user(self.message.author.id)
                self.user_data = config_data.UserData()

            cache[self.message.author.id] = self.user_data

    async def get_data(self):
        """Combine three data-gathering functions into one."""
        await self.get_user_data()

        if self.message.guild is not None:
            await self.get_channel_data()
            await self.get_guild_data()

            if self.message.channel.category_id is not None:
                await self.get_category_data()

    async def clear_cache(self):
        """Clear cache."""
        await self.user_data.clear_cache()
        await self.channel_data.clear_cache()
        await self.category_data.clear_cache()
        await self.guild_data.clear_cache()

        self._prefix = None
        self._language_id = None
        self._language = None
