"""Import stuff."""
import asyncio
import discord

from bot.data import definitions
from framework import embeds


class Argument():
    """
    Contains essential information for arguments.

    Default values and such are defined in argument rules.
    """

    def __init__(self, obj_id=None, modification=None):
        """Initialise object."""
        self.obj_id = obj_id
        self.modification = modification

        self.localisation = {}

    def add_localisation(self, language_id, argument_localisation):
        """Add argument localisation."""
        self.localisation[language_id] = {}
        localisation = self.localisation[language_id]

        localisation["name"] = argument_localisation["name"]
        localisation["description"] = argument_localisation["description"]

    async def convert(self, argument, context):
        """Convert the argument from raw string to what it is supposed to be."""
        converted_argument = argument
        if self.modification is not None:
            converted_argument = await self.modification(argument, context)

        return converted_argument

    async def dialogue(
            self, context, optional_argument, argument_number, total_arguments):
        """
        Handle dialogue for argument input.

        If user wants to cancel, then the big X should be pressed.
        """
        if argument_number > total_arguments:
            argument_number = total_arguments

        emoji = None
        if optional_argument:
            emoji = "✅"
        else:
            emoji = "❌"

        desc = None
        if optional_argument:
            desc = await context.language.get_text("confirm_to_stop")
        else:
            desc = await context.language.get_text("cancel_to_abort")

        message = embeds.PaginatedEmbed(
            await context.language.get_text(
                "argument_number",
                {"arg": argument_number, "total_arg": total_arguments}))

        message.embed.title = self.localisation[context.language_id]["description"]
        message.embed.description = desc

        dialogue_msg = await message.send(context)
        await dialogue_msg.add_reaction(emoji)

        def msg_check(message):
            """Check if the message sent is from the command user."""
            return (message.author == context.message.author and
                    message.channel == context.message.channel)

        def reaction_check(reaction, user):
            """Check if the reaction is from the command user."""
            return (reaction.message.id == dialogue_msg.id and
                    reaction.emoji == emoji and
                    user == context.message.author)

        done, pending = await asyncio.wait(
            [definitions.CLIENT.wait_for("message", check=msg_check),
             definitions.CLIENT.wait_for("reaction_add", check=reaction_check)],
            return_when=asyncio.FIRST_COMPLETED)

        response = done.pop().result()

        argument = None
        if isinstance(response, discord.Message):
            argument = response.content

        for future in pending:
            future.cancel()  # We do not need these anymore.

        return argument
