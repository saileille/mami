"""Import stuff."""
from bot.database import database_functions
from bot.data import default_values
from bot.data import definitions
from datatypes import config_data


class Context():
    """Contains configuration data and the message."""

    def __init__(
            self, message=None, user_data=None, channel_data=None, category_data=None,
            guild_data=None, timestamp=None):
        """Initialise object."""
        self.message = message
        self.user_data = user_data
        self.channel_data = channel_data
        self.category_data = category_data
        self.guild_data = guild_data
        self.timestamp = timestamp

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

    async def get_category_data(self, category_id):
        """
        Get the category data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["categories"]
        if category_id in cache:
            self.category_data = cache[category_id]
        else:
            self.category_data = await database_functions.select_category(category_id)

            if self.category_data is None:
                await database_functions.insert_category(category_id)
                self.category_data = config_data.CategoryData()

            cache[category_id] = self.category_data

    async def get_channel_data(self, channel_id):
        """
        Get the channel data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["channels"]
        if channel_id in cache:
            self.channel_data = cache[channel_id]
        else:
            self.channel_data = await database_functions.select_channel(channel_id)

            if self.channel_data is None:
                await database_functions.insert_channel(channel_id)
                self.channel_data = config_data.ChannelData()

            cache[channel_id] = self.channel_data

    async def get_guild_data(self, guild_id):
        """
        Get the guild data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["guilds"]
        if guild_id in cache:
            self.guild_data = cache[guild_id]
        else:
            self.guild_data = await database_functions.select_guild(guild_id)

            if self.guild_data is None:
                await database_functions.insert_guild(guild_id)
                self.guild_data = config_data.GuildData()

            cache[guild_id] = self.guild_data

    async def get_user_data(self, user_id):
        """
        Get the user data.

        The function goes through cache, then database, and finally creates a new entry if
        one does not exist. Also adds an entry to the cache.
        """
        cache = definitions.DATA_CACHE["users"]
        if user_id in cache:
            self.user_data = cache[user_id]
        else:
            self.user_data = await database_functions.select_user(user_id)

            if self.user_data is None:
                await database_functions.insert_user(user_id)
                self.user_data = config_data.UserData()

            cache[user_id] = self.user_data

    async def get_data(self):
        """Combine three data-gathering functions into one."""
        await self.get_user_data(self.message.author.id)

        if self.message.guild is not None:
            await self.get_channel_data(self.message.channel.id)
            await self.get_guild_data(self.message.guild.id)

            if self.message.channel.category_id is not None:
                await self.get_category_data(self.message.channel.category_id)

    async def clear_cache(self):
        """Clear cache."""
        await self.user_data.clear_cache()
        await self.channel_data.clear_cache()
        await self.category_data.clear_cache()
        await self.guild_data.clear_cache()

        self._prefix = None
        self._language_id = None
        self._language = None


async def get_context_from_channel(channel):
    """Get context data from channel alone."""
    context = Context()

    await context.get_channel_data(channel.id)
    await context.get_guild_data(channel.guild.id)

    if channel.category_id is not None:
        await context.get_category_data(channel.category_id)

    return context
