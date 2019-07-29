"""Embed-related functions and classes."""
import asyncio
from math import ceil
from random import randint
import discord

from bot.data import default_values
from bot.data import definitions


class EmbedFieldCollection():
    """Collection of one or more embed fields that can be inline together."""

    def __init__(self, content_list, title, column_amount=1):
        """Initialise object."""
        if isinstance(content_list, list):
            self.content_list = content_list
        else:
            self.content_list = [content_list]

        self.title = title
        self.column_amount = column_amount

        self.columns = []
        self.paginate()

    @property
    def inline(self):
        """
        Check if the embed fields are supposed to be inline.

        Column amount of 1 will never be inline, more than 1 will always be inline.
        """
        return self.column_amount != 1

    @property
    def pages(self):
        """Get the amount of pages the fields need to display all information."""
        return ceil(len(self.columns) / self.column_amount)

    def paginate(self):
        """Paginate columns."""
        self.columns = []

        zero_index = 0
        new_rows = []
        column_full = False
        for i, content in enumerate(self.content_list):
            row_index = i % self.column_amount
            column_index = zero_index + row_index

            if len(self.columns) < column_index + 1:
                self.columns.append(content)
            else:
                new_content = "\n" + content
                if len(self.columns[column_index] + new_content) > default_values.EMBED_FIELD_MAX_SIZE:
                    column_full = True

                new_rows.append(new_content)

            if len(new_rows) == self.column_amount or i == len(self.content_list) - 1:
                if column_full:
                    zero_index += self.column_amount
                    for row in new_rows:
                        self.columns.append(row.strip())
                else:
                    for j, row in enumerate(new_rows):
                        self.columns[zero_index + j] += row

                column_full = False
                new_rows = []

    async def set_page(self, page, embed):
        """Add the column info of a certain page."""
        first_index = self.column_amount * page
        last_index = self.column_amount * (page + 1)

        for i in range(first_index, last_index):
            if i == len(self.columns):
                break

            embed.add_field(name=self.title, value=self.columns[i], inline=self.inline)

        return embed


class PaginatedEmbed():
    """Embed with pagination."""

    def __init__(self, author_text, *fields):
        """Initialise object."""
        self._author_text = author_text
        self.fields = list(fields)

        self.embed = discord.Embed()
        self.message = None
        self.current_page = 0

    @property
    def pages(self):
        """Get the amount of pages the embed needs to display all information."""
        pages = 1
        for field in self.fields:
            field_pages = field.pages
            if field_pages > pages:
                pages = field_pages

        return pages

    @property
    def author_text(self):
        """Get the appropriate page title."""
        pages = self.pages
        if pages > 1:
            page = self.current_page + 1
            return self._author_text + " [{page}/{page_total}]".format(
                page=page, page_total=pages)

        return self._author_text

    async def send(self, context, thumbnail="default", colour=None):
        """Send an embed message with as much automation as possible."""
        if thumbnail == "default":
            thumbnail = context.message.author.avatar_url

        await self.pre_message(context, thumbnail, colour)
        self.message = await context.message.channel.send("", embed=self.embed)
        await self.post_message(context)

        return self.message

    async def pre_message(self, context, thumbnail, colour):
        """Initialise the embed."""
        if colour is None:
            colour = await get_random_colour()

        icon_url = context.message.author.avatar_url
        if context.message.guild is not None:
            icon_url = context.message.guild.icon_url

        self.embed.colour = colour
        self.embed.set_footer(
            text=await context.language.get_text("calculating"),
            icon_url=definitions.CLIENT.user.avatar_url)

        if thumbnail:
            self.embed.set_thumbnail(url=thumbnail)

        await self.update_page(icon_url)

    async def post_message(self, context):
        """Post-message handling."""
        msg_time = None
        if context.message.edited_at is not None:
            msg_time = context.message.edited_at
        else:
            msg_time = context.message.created_at

        context.ping = int((self.message.created_at - msg_time).total_seconds() * 1000)

        icon = self.embed.footer.icon_url
        self.embed.set_footer(
            text=await context.language.get_text("ping", {"ping": context.ping}),
            icon_url=icon)

        await self.message.edit(embed=self.embed)

        if self.pages > 1:
            await self.paginator(context.message)

    async def update_page(self, icon_url=None):
        """Update the fields to the current page."""
        if icon_url is None:
            icon_url = self.embed.author.icon_url

        self.embed.clear_fields()
        for field in self.fields:
            await field.set_page(self.current_page, self.embed)

        self.embed.set_author(name=self.author_text, icon_url=icon_url)
        if self.message is not None:
            await self.message.edit(embed=self.embed)

    async def paginator(self, user_message):
        """Set up controls for browsing message pages."""
        pages = self.pages

        while True:
            emoji_list = []
            if self.current_page != 0:
                emoji_list.append("◀")
            elif self.current_page + 1 != pages:
                emoji_list.append("▶")

            def check(reaction, user):
                return (
                    reaction.message.id == self.message.id and
                    user == user_message.author and
                    reaction.emoji in emoji_list)

            for emoji in emoji_list:
                await self.message.add_reaction(emoji)
            try:
                reaction, user = await definitions.CLIENT.wait_for(
                    "reaction_add", timeout=60, check=check)

                if reaction.emoji == "◀":
                    self.current_page -= 1
                elif reaction.emoji == "▶":
                    self.current_page += 1

                await self.message.clear_reactions()
                await self.update_page()

            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                break


async def get_random_colour():
    """Return a random Discord colour."""
    rgb = []
    while len(rgb) < 3:
        rgb.append(randint(0, 255))

    return discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])
