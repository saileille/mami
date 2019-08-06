"""Guild-call-related mechanics."""
from discord import Embed


class GuildCall():
    """Guild call object."""

    def __init__(self, connected_channel=None, connecting=False):
        """Initialise object."""
        self.connected_channel = connected_channel
        self.connecting = connecting
        self.messages = {}

    def __str__(self):
        """Get string representation of the object."""
        return ("Connected Channel: {self.connected_channel}\n"
                "Connecting: {self.connecting}").format(self=self)

    async def relay_message(self, message):
        """Send the message to the connected channel."""
        remote_message = await self.connected_channel.send(
            embed=await get_message(message))

        self.messages[message.id] = remote_message

    async def edit_message(self, message):
        """Edit a sent message in the other server."""
        remote_message = None
        try:
            remote_message = self.messages[message.id]
        except KeyError:
            return

        await remote_message.edit(embed=await get_message(message))

    async def delete_message(self, message):
        """Delete a sent message in the connected channel."""
        remote_message = None
        try:
            remote_message = self.messages[message.id]
        except KeyError:
            return

        await remote_message.delete()

    async def typing(self):
        """Send typing to the connected channel."""
        await self.connected_channel.trigger_typing()


async def get_message(message):
    """Get the message to be sent to the connected channel."""
    embed = Embed()

    embed.set_author(name=message.author, icon_url=message.author.avatar_url)
    embed.description = "📞 " + message.content

    embed.colour = message.author.colour
    if str(embed.colour) == "#000000":
        embed.colour = Embed.Empty

    return embed
