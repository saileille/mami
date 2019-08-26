"""Rune-related functions."""
from bot.data import default_values


async def translate_archaic(context, arguments):
    """Translate text to archaic runes."""
    return await translate(context, arguments, "archaic")


async def translate_modern(context, arguments):
    """Translate text to modern runes."""
    return await translate(context, arguments, "modern")


async def translate_musical(context, arguments):
    """Translate text to musical runes."""
    return await translate(context, arguments, "musical")


async def translate(context, arguments, style):
    """Translate text to any set of runes."""
    large_font_spaces = 5
    small_font_spaces = int(27 / 40 * large_font_spaces)
    large_font = True

    text = arguments[0]
    runes = ""

    rune_count = 0
    for i, char in enumerate(text.lower()):
        if char in default_values.RUNES[style]:
            runes += default_values.RUNES[style][char]
            rune_count += 1
        elif char in default_values.RUNES["archaic"]:
            runes += default_values.RUNES["archaic"][char]
            rune_count += 1
        else:
            runes += text[i]
            if char != " ":
                large_font = False

    if not context.desktop_ui or not large_font or rune_count > 27:
        runes = runes.replace(" ", " " * small_font_spaces)
    else:
        runes = runes.replace(" ", " " * large_font_spaces)

    await context.message.channel.send(runes)
    return True
