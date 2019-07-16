"""
Miscellaneous functions.

Should be moved elsewhere once a trend emerges.
"""
from random import randint
from discord import Colour
from bot.data import definitions


async def get_random_colour():
    """Return a random Discord colour."""
    rgb = []
    while len(rgb) < 3:
        rgb.append(randint(0, 255))

    return Colour.from_rgb(rgb[0], rgb[1], rgb[2])


async def pre_message(context, author_text, embed, thumbnail, colour):
    """Initialise the embed."""
    if colour is None:
        colour = await get_random_colour()

    icon_url = context.message.author.avatar_url
    if context.message.guild is not None:
        icon_url = context.message.guild.icon_url

    embed.colour = colour
    embed.set_footer(
        text=await context.get_language_text("calculating"),
        icon_url=definitions.CLIENT.user.avatar_url)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    embed.set_author(name=author_text, icon_url=icon_url)


async def post_message(context, msg, embed):
    """Post-message handling."""
    msg_time = None
    if context.message.edited_at is not None:
        msg_time = context.message.edited_at
    else:
        msg_time = context.message.created_at

    context.ping = int((msg.created_at - msg_time).total_seconds() * 1000)

    icon = embed.footer.icon_url
    embed.set_footer(text=await context.get_language_text("ping"), icon_url=icon)
    await msg.edit(embed=embed)


async def send(context, author_text, embed, thumbnail="default", colour=None):
    """Send an embed message with as much automation as possible."""
    if thumbnail == "default":
        thumbnail = context.message.author.avatar_url

    await pre_message(context, author_text, embed, thumbnail, colour)
    msg = await context.message.channel.send("", embed=embed)
    await post_message(context, msg, embed)

    return msg
