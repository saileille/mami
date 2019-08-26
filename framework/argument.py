"""Import stuff."""
import asyncio
import discord

from bot.data import default_values
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
        self.localisation[language_id] = argument_localisation
        localisation = self.localisation[language_id]

        if "bonus_fields" in argument_localisation:
            localisation["bonus_fields"] = argument_localisation["bonus_fields"]

        localisation["name"] = argument_localisation["name"]
        localisation["description"] = argument_localisation["description"]
        localisation["help_text"] = argument_localisation["help_text"]

    def create_language_data(self, language_id):
        """Create the language data template for a given argument."""
        default_localisation = None
        if default_values.LANGUAGE_ID in self.localisation:
            default_localisation = self.localisation[default_values.LANGUAGE_ID]
        elif language_id == default_values.LANGUAGE_ID:
            default_localisation = {"name": "", "description": "", "help_text": ""}

        localisation = {
            "name": default_localisation["name"],
            "description": default_localisation["description"],
            "help_text": default_localisation["help_text"]}

        if "bonus_fields" in default_localisation:
            localisation["bonus_fields"] = default_localisation["bonus_fields"]

        return localisation

    async def get_info_embed_field(self, context, argument_no):
        """Get the embed field of the argument for command info."""
        localisation = self.localisation[context.language_id]

        return embeds.EmbedFieldCollection(
            localisation["help_text"],
            await context.language.get_text(
                "argument_name_and_number",
                {"name": localisation["name"], "number": argument_no}))

    async def convert(self, argument, context):
        """Convert the argument from raw string to what it is supposed to be."""
        converted_argument = argument
        if self.modification is not None:
            converted_argument = await self.modification(argument, context)

        return converted_argument

    async def dialogue(
            self, context, optional_argument, argument_number, total_arguments):
        """Send a message about the argument to the user and wait for response."""
        if argument_number > total_arguments:
            argument_number = total_arguments

        emoji = None
        desc_key = None
        if optional_argument:
            emoji = "✅"
            desc_key = "confirm_to_stop"
        else:
            emoji = "❌"
            desc_key = "cancel_to_abort"

        message = embeds.PaginatedEmbed(
            await context.language.get_text(
                "argument_number",
                {"arg": argument_number, "total_arg": total_arguments}))

        localisation = self.localisation[context.language_id]
        message.embed.title = localisation["description"]
        message.embed.description = await context.language.get_text(desc_key)

        if "bonus_fields" in localisation:
            await Argument.add_dialogue_bonus_fields(context, message, localisation)

        dialogue_msg = await message.send(context)
        await dialogue_msg.add_reaction(emoji)

        return await Argument.dialogue_response(context, dialogue_msg, emoji)

    @staticmethod
    async def add_dialogue_bonus_fields(context, message, localisation):
        """Add the bonus fields in the dialogue message."""
        for field in localisation["bonus_fields"]:
            content_list = field["content"]
            if content_list == "var_all_languages":
                content_list = await context.language.get_all_languages()

            message.fields.append(embeds.EmbedFieldCollection(
                content_list, field["title"], column_amount=2))

    @staticmethod
    async def dialogue_response(context, dialogue_msg, emoji):
        """Handle the waiting of a dialogue response."""
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
            return_when=asyncio.FIRST_COMPLETED, timeout=60)

        response = None
        try:
            response = done.pop().result()
        except KeyError:
            pass

        await definitions.CLIENT.remove_reactions(
            await context.message.channel.fetch_message(dialogue_msg.id), emoji)

        argument = None
        if isinstance(response, discord.Message):
            argument = response.content
            context.timestamp = response.created_at

        for future in pending:
            future.cancel()  # We do not need these anymore.

        return argument
