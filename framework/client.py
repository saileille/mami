"""Import stuff."""
import asyncio
import random
import time

import aiohttp
import discord

from bot.data import cache
from bot.data import default_values
from bot.data import definitions
from bot.data import secrets
from bot.mechanics import auto_convert
from framework import context
from framework import custom_json
from framework import command_handler


class Client(discord.Client):
    """Customised client class."""

    def __init__(self, *args, **kwargs):
        """Initialise object."""
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.currency_check_task = self.loop.create_task(self.currency_check())
        self.playing_message_task = self.loop.create_task(self.change_playing_msg())

    async def on_ready(self):
        """Notify me when client is ready."""
        print("Connected.")

    async def on_message(self, message):
        """Pass on incoming messages."""
        await Client.handle_message(message)

    async def on_message_edit(self, old, new):
        """Pass on incoming message edits."""
        if old.content == new.content:
            return

        await Client.handle_message(new, edit=True)

    async def on_message_delete(self, message):
        """Handle deleted messages."""
        context_obj = context.Context(message)
        await context_obj.get_data()

        if context_obj.channel_data.guild_call.connected_channel is not None:
            await context_obj.channel_data.guild_call.delete_message(message)

    async def on_typing(self, channel, user, when):
        """Handle typing."""
        if user.bot:
            return

        context_obj = await context.get_context_from_channel(channel)
        if context_obj.channel_data.guild_call.connected_channel is not None:
            await context_obj.channel_data.guild_call.typing()

    async def on_reaction_add(self, reaction, user):
        """Handle reaction-adds in certain cases."""
        if user.bot:
            return

        if reaction.emoji == "ℹ":
            context_obj = context.Context(reaction.message)
            await context_obj.get_data()
            await auto_convert.send_conversion(context_obj, user.id)

    @staticmethod
    async def handle_message(message, edit=False):
        """Handle incoming messages."""
        # Mami does not deal with bots.
        if message.author.bot:
            return

        context_obj = context.Context(message)
        await context_obj.get_data()
        if edit:
            context_obj.timestamp = message.edited_at
        else:
            context_obj.timestamp = message.created_at

        command_string = await command_handler.check_prefix(context_obj)

        if command_string is not None:
            await command_handler.process_command_call(context_obj, command_string)
            return

        await auto_convert.detect_unit_mention(context_obj)

        if context_obj.channel_data.guild_call.connected_channel is not None:
            if edit:
                await context_obj.channel_data.guild_call.edit_message(message)
            else:
                await context_obj.channel_data.guild_call.relay_message(message)

    async def currency_check(self):
        """Update the currency API data on fixed intervals."""
        await self.wait_until_ready()
        print("Starting the currency data update loop...")

        timer_data = custom_json.load("bot\\database\\currency_api\\timer.json")

        current_time = time.time()
        if "next_check" not in timer_data or timer_data["next_check"] < current_time:
            timer_data["interval"] = timer_data["default_interval"]
            timer_data["next_check"] = current_time
            await Client.get_latest_currency_data(timer_data)
        else:
            cache.CURRENCY_DATA = custom_json.load(
                "bot\\database\\currency_api\\data.json")

            timer_data["interval"] = timer_data["next_check"] - current_time

        while not self.is_closed():
            await asyncio.sleep(timer_data["interval"])
            timer_data["interval"] = timer_data["default_interval"]

            await Client.get_latest_currency_data(timer_data)

    async def change_playing_msg(self):
        """Update the playing message on fixed intervals."""
        await self.wait_until_ready()
        print("Starting the playing message loop...")

        while not self.is_closed():
            language_id = random.choice(list(definitions.LANGUAGES))
            await self.change_presence(
                activity=discord.Game(
                    name=await definitions.LANGUAGES[language_id].get_text(
                        "playing_message", {"prefix": default_values.PREFIX})))

            await asyncio.sleep(30)

    @staticmethod
    async def get_latest_currency_data(timer_data):
        """
        Get the latest currency data from the API.

        Also updates the timer and saves the updated currency data.
        """
        timer_data["next_check"] += timer_data["default_interval"]

        custom_json.save(timer_data, "bot\\database\\currency_api\\timer.json")

        cache.CURRENCY_DATA = {}
        api_key = secrets.CURRENCY_API_KEY

        async with aiohttp.ClientSession() as session:
            url = "http://data.fixer.io/api/latest?access_key=" + api_key
            async with session.get(url) as request:
                rates = await request.json()
                cache.CURRENCY_DATA["timestamp"] = rates["timestamp"]
                cache.CURRENCY_DATA["currencies"] = {}

                for key in rates["rates"]:
                    cache.CURRENCY_DATA["currencies"][key] = {
                        "code": key, "rate": rates["rates"][key]}

            url = "http://data.fixer.io/api/symbols?access_key=" + api_key
            async with session.get(url) as request:
                names = await request.json()
                for key in names["symbols"]:
                    cache.CURRENCY_DATA["currencies"][key]["name"] = names["symbols"][key]

        custom_json.save(cache.CURRENCY_DATA, "bot\\database\\currency_api\\data.json")

    @staticmethod
    async def remove_reactions(message, *emojis):
        """Remove all reactions of the given emojis from a message."""
        for reaction in message.reactions:
            if reaction.emoji in emojis:
                async for user in reaction.users():
                    await reaction.remove(user)
