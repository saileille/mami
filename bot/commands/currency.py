"""Currency commands."""
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

    message = embeds.PaginatedEmbed(
        await context.language.get_text(
            "convert_currency_title",
            {"base": base_currency["code"], "target": target_currency["code"]}))

    formatted_base_amount = await context.language.format_number(
        amount, decimal_rules=".2f")
    formatted_target_amount = await context.language.format_number(
        converted_amount, decimal_rules=".2f")

    base = await context.language.get_text(
        "unit_representation",
        {"unit_amount": formatted_base_amount, "unit_name": base_currency["name"]})

    target = await context.language.get_text(
        "unit_representation",
        {"unit_amount": formatted_target_amount, "unit_name": target_currency["name"]})

    message.embed.description = ":currency_exchange: " + await context.language.get_text(
        "unit_conversion", {"unit_and_amount": base, "conversion_list": target})

    await message.send(context)


async def view_all(context, command_input):
    """Display all currencies."""
    currencies = []

    columns = 1
    thumbnail = True
    if context.desktop_ui:
        columns = 2
        thumbnail = False

    for key, value in cache.CURRENCY_DATA["currencies"].items():
        currencies.append(key + " - " + value["name"])

    currencies.sort()
    embed = embeds.PaginatedEmbed(
        await context.language.get_text("view_all_currencies_title"),
        embeds.EmbedFieldCollection(
            currencies, await context.language.get_text("currencies_title"), columns))

    embed.embed.description = await context.language.get_text("view_all_currencies_desc")
    await embed.send(context, thumbnail=thumbnail)
