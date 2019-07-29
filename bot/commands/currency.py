"""Currency commands."""
from aid import numbers
from bot.data import cache
from framework import embeds


async def convert(context, arguments):
    """Convert from one currency to another."""
    amount = arguments[0]
    base_currency = arguments[1]
    target_currency = arguments[2]

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


async def search(context, arguments):
    """Search currencies with search terms."""
    search_term = arguments[0]
    currencies = []

    columns = 1
    thumbnail = True
    if context.desktop_ui:
        columns = 2
        thumbnail = False

    search_term_lower = search_term.lower()
    for key, value in cache.CURRENCY_DATA["currencies"].items():
        if search_term_lower in value["name"].lower():
            currencies.append(key + " - " + value["name"])

    currencies.sort()
    message = embeds.PaginatedEmbed(
        await context.language.get_text("search_currencies_title"),
        embeds.EmbedFieldCollection(
            currencies, await context.language.get_text("currencies_title"), columns))

    message.embed.description = await context.language.get_text(
        "search_currencies_desc", {"search_term": search_term})

    await message.send(context, thumbnail=thumbnail)


async def view_all(context, arguments):
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
    message = embeds.PaginatedEmbed(
        await context.language.get_text("view_all_currencies_title"),
        embeds.EmbedFieldCollection(
            currencies, await context.language.get_text("currencies_title"), columns))

    message.embed.description = await context.language.get_text(
        "view_all_currencies_desc")

    await message.send(context, thumbnail=thumbnail)
