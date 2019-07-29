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
from framework import custom_json
from framework import command_handler
from framework.context import Context


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

        await Client.handle_message(new)

    async def on_reaction_add(self, reaction, user):
        """Handle reaction-adds in certain cases."""
        if user.bot:
            return

        if reaction.emoji == "ℹ":
            context = Context(reaction.message)
            await context.get_data()
            await auto_convert.send_conversion(context, user.id)

    @staticmethod
    async def handle_message(message):
        """Handle incoming messages."""
        # Mami does not deal with bots.
        if message.author.bot:
            return

        context = Context(message)
        await context.get_data()

        command_string = await command_handler.check_prefix(context)

        if command_string is not None:
            await command_handler.process_command_call(context, command_string)

        if command_string is None:
            await auto_convert.detect_unit_mention(context)
            return

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
