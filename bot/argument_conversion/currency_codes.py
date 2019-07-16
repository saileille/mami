"""Conversions of currency codes and such."""
from bot.data import cache
from bot.misc import embed_messages


async def valid_currency(argument, context):
    """
    Check if the argument is a valid currency.

    If valid, return the currency data.
    """
    currency = None
    if argument not in cache.CURRENCY_DATA["currencies"]:
        custom_msg = await context.get_language_text("invalid_currency")
        await embed_messages.invalid_argument(context, argument, custom_msg)
    else:
        currency = cache.CURRENCY_DATA["currencies"][argument]

    return currency
