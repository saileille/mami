"""Guild-call-related commands."""
from bot.data import definitions


async def new_guild_call(context, arguments):
    """"""
    context.channel_data.guild_call.connecting = True
    for key, channel in definitions.DATA_CACHE["channels"].items():
        channel_object = definitions.CLIENT.get_channel(key)
        valid_channel = (
            channel.guild_call.connecting and
            channel.guild_call.connected_channel is None and
            context.message.guild.id != channel_object.guild.id)

        if valid_channel:
            channel.guild_call.connected_channel = context.message.channel.id
            channel.guild_call.connecting = False

            context.channel_data.guild_call.connected_channel = key
            context.channel_data.guild_call.connecting = False

            # Send messages to both channels indicating they can now talk.
