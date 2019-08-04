"""Guild-call-related commands."""
from bot.data import definitions
from framework import context
from framework import embeds


async def connect_guild_call(context_obj, arguments):
    """Try to connect to a guild call."""
    disconnect_cmd = await definitions.COMMANDS.get_sub_command_from_path(
        "guild_call", "disconnect")

    context_obj.channel_data.guild_call.connecting = True

    cmd_user_msg = embeds.PaginatedEmbed(
        await context_obj.language.get_text("guild_call_connecting_title"))
    cmd_user_msg.embed.description = "📡 " + await context_obj.language.get_text(
        "guild_call_connecting_desc",
        {"disconnect_cmd": await disconnect_cmd.get_command_string(context_obj)})

    await cmd_user_msg.send(context_obj)

    for key, channel_data in definitions.DATA_CACHE["channels"].items():
        channel_object = definitions.CLIENT.get_channel(key)
        valid_channel = (
            channel_data.guild_call.connecting and
            channel_data.guild_call.connected_channel is None and
            context_obj.message.guild.id != channel_object.guild.id)

        if valid_channel:
            channel_data.guild_call.connected_channel = context_obj.message.channel
            context_obj.channel_data.guild_call.connected_channel = channel_object
            channel_data.guild_call.connecting = False
            context_obj.channel_data.guild_call.connecting = False

            # Send messages to both channels indicating they can now talk.

            cmd_user_msg = embeds.PaginatedEmbed(
                await context_obj.language.get_text("guild_call_connected_title"))

            cmd_user_msg.embed.description = await context_obj.language.get_text(
                "guild_call_connected_desc")

            contact_context = await context.get_context_from_channel(channel_object)
            contact_channel_msg = embeds.PaginatedEmbed(
                await contact_context.language.get_text("guild_call_connected_title"))

            contact_channel_msg.embed.description = await context_obj.language.get_text(
                "guild_call_connected_desc")

            await cmd_user_msg.send(context_obj, thumbnail=channel_object.guild.icon_url)
            await contact_channel_msg.send(
                contact_context, channel=channel_object,
                thumbnail=context_obj.message.guild.icon_url,
                author_icon=channel_object.guild.icon_url)

            break


async def disconnect_guild_call(context_obj, arguments):
    """Hang up or stop trying to connect the call."""
    context_obj.channel_data.guild_call.connecting = False

    cmd_user_msg = embeds.PaginatedEmbed(await context_obj.language.get_text(
        "guild_call_disconnected_title"))
    cmd_user_msg.embed.description = await context_obj.language.get_text(
        "guild_call_disconnected_desc")

    if context_obj.channel_data.guild_call.connected_channel is not None:
        connected_channel = context_obj.channel_data.guild_call.connected_channel
        connected_context = await context.get_context_from_channel(connected_channel)

        context_obj.channel_data.guild_call.messages = {}
        connected_context.channel_data.guild_call.messages = {}

        context_obj.channel_data.guild_call.connected_channel = None
        connected_context.channel_data.guild_call.connected_channel = None
        connected_context.channel_data.guild_call.connecting = False

        connected_msg = embeds.PaginatedEmbed(
            await connected_context.language.get_text(
                "other_party_disconnected_guild_call_title"))

        connected_msg.embed.description = await connected_context.language.get_text(
            "other_party_disconnected_guild_call_desc")

        await connected_msg.send(
            connected_context, channel=connected_channel,
            thumbnail=context_obj.message.guild.icon_url,
            author_icon=connected_channel.guild.icon_url)

    await cmd_user_msg.send(context_obj)
