"""Currency commands."""
import discord

from aid import lists
from aid import numbers
from bot.data import cache
from framework import embeds


async def convert(context, command_input):
    """Convert from one currency to another."""
    amount = command_input.arguments[0]
    base_currency = command_input.arguments[1]
    target_currency = command_input.arguments[2]

    converted_amount = await numbers.convert(
        amount, base_currency["rate"], target_currency["rate"])

    embed = discord.Embed()

    formatted_base_amount = await context.language.format_number(
        amount, decimal_rules=".2f")
    formatted_target_amount = await context.language.format_number(
        converted_amount, decimal_rules=".2f")

    base = await context.get_language_text(
        "unit_representation",
        {"unit_amount": formatted_base_amount, "unit_name": base_currency["name"]})

    target = await context.get_language_text(
        "unit_representation",
        {"unit_amount": formatted_target_amount, "unit_name": target_currency["name"]})

    embed.description = ":currency_exchange: " + await context.get_language_text(
        "unit_conversion", {"unit_and_amount": base, "conversion_list": target})

    await embeds.send(
        context,
        await context.get_language_text(
            "convert_currency_title",
            {"base": base_currency["code"], "target": target_currency["code"]}),
        embed)


async def view_all(context, command_input):
    """Display all currencies."""
    currencies = []
    columns = 4
    for key, value in cache.CURRENCY_DATA["currencies"].items():
        currencies.append(key + " - " + value["name"])

    currencies.sort()
    column_strings = await lists.divide_into_columns(currencies, columns)

    embed = discord.Embed()
    for column_string in column_strings:
        embed.add_field(
            name=await context.get_language_text("currencies_title"),
            value=column_string)

    embed.description = await context.get_language_text("view_all_currencies_desc")

    await embeds.send(
        context,
        await context.get_language_text("view_all_currencies_title"),
        embed,
        thumbnail=False)
