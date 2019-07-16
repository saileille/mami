"""Import stuff."""
from bot.database import database_functions
from bot.data import default_values
from bot.data import definitions
from datatypes import config_data


class Context():
    """Contains configuration data and the message."""

    def __init__(self,
                 message):
        """Initialise object."""
        self.message = message
        self.user_data = None
        self.channel_data = None
        self.category_data = None
        self.guild_data = None
        self.ping = None

        self._prefix = None
        self._language_id = None
        self._language = None
        self._max_dice = None

    @property
    def prefix(self):
        """Get the command prefix."""
        if self._prefix is None:
            if self.user_data.prefix is not None:
                self._prefix = self.user_data.prefix

            elif self.message.guild is not None:
                if self.channel_data.prefix is not None:
                    self._prefix = self.channel_data.prefix
                elif self.category_data.prefix is not None:
                    self._prefix = self.category_data.prefix
                elif self.guild_data.prefix is not None:
                    self._prefix = self.guild_data.prefix
                else:
                    self._prefix = default_values.PREFIX
            else:
                self._prefix = default_values.PREFIX

        return self._prefix

    @property
    def language_id(self):
        """Get the language ID."""
        if self._language_id is None:
            if self.user_data.language_id is not None:
                self._language_id = self.user_data.language_id

            elif self.message.guild is not None:
                if self.channel_data.language_id is not None:
                    self._language_id = self.channel_data.language_id
                elif self.category_data.language_id is not None:
                    self._language_id = self.category_data.language_id
                elif self.guild_data.language is not None:
                    self._language_id = self.guild_data.language_id
                else:
                    self._language_id = default_values.LANGUAGE_ID

            else:
                self._language_id = default_values.LANGUAGE_ID

        return self._language_id

    @property
    def language(self):
        """Get the language object."""
        if self._language is None:
            self._language = definitions.LANGUAGES[self.language_id]

        return self._language

    @property
    def max_dice(self):
        """Get the maximum amount of dice one can use."""
        if self._max_dice is None:
            if self.channel_data.max_dice is not None:
                self._max_dice = self.channel_data.max_dice
            elif self.category_data.max_dice is not None:
                self._max_dice = self.category_data.max_dice
            elif self.guild_data.max_dice is not None:
                self._max_dice = self.guild_data.max_dice
            else:
                self._max_dice = default_values.MAX_DICE

        return self._max_dice

    async def check_command_rules(self, command_id_list):
        """
        Check the command rules.

        Returns whether the command is allowed or not, and a
        list of the IDs leading to the last allowed command.
        """
        allow = await self.channel_data.check_command_rules(
            self.message, command_id_list)
        if allow is None:
            allow = await self.category_data.check_command_rules(
                self.message, command_id_list)
        if allow is None:
            allow = await self.guild_data.check_command_rules(
                self.message, command_id_list)
        return allow

    async def get_user_data(self):
        """Get the user data from the database, or create new entry."""
        self.user_data = await database_functions.select_user(self.message.author.id)

        if self.user_data is None:
            await database_functions.insert_user(self.message.author.id)
            self.user_data = config_data.UserData()

    async def get_channel_data(self):
        """Get the channel data from the database, or create new entry."""
        self.channel_data = await database_functions.select_channel(
            self.message.channel.id)

        if self.channel_data is None:
            await database_functions.insert_channel(self.message.channel.id)
            self.channel_data = config_data.ChannelData()

    async def get_category_data(self):
        """Get the category data from the database, or create new entry."""
        self.category_data = await database_functions.select_category(
            self.message.channel.category_id)

        if self.category_data is None:
            await database_functions.insert_category(self.message.channel.category_id)
            self.category_data = config_data.CategoryData()

    async def get_guild_data(self):
        """Get the guild data from the database, or create new entry."""
        self.guild_data = await database_functions.select_guild(self.message.guild.id)

        if self.guild_data is None:
            await database_functions.insert_guild(self.message.guild.id)
            self.guild_data = config_data.GuildData()

    async def get_data(self):
        """Combine three data-gathering functions into one."""
        await self.get_user_data()

        if self.message.guild is not None:
            await self.get_channel_data()
            await self.get_category_data()
            await self.get_guild_data()

    async def clear_cache(self):
        """Clear cache."""
        await self.user_data.clear_cache()
        await self.channel_data.clear_cache()
        await self.category_data.clear_cache()
        await self.guild_data.clear_cache()

        self._prefix = None
        self._language_id = None
        self._language = None

    async def get_language_text(self, key, variables=None):
        """Get text from the context language."""
        if variables is None:
            variables = {}

        text = await self.language.get_text(key)
        return text.format(context=self, **variables)
