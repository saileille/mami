"""Rune-related functions."""
from bot.data import default_values


async def translate_archaic(context, command_input):
    """Translate text to archaic runes."""
    runes = await translate(context, command_input, "archaic")
    await context.message.channel.send(runes)


async def translate_modern(context, command_input):
    """Translate text to modern runes."""
    runes = await translate(context, command_input, "modern")
    await context.message.channel.send(runes)


async def translate_musical(context, command_input):
    """Translate text to musical runes."""
    runes = await translate(context, command_input, "musical")
    await context.message.channel.send(runes)


async def translate(context, command_input, style):
    """Translate text to any set of runes."""
    large_font_spaces = 5
    small_font_spaces = int(27 / 40 * large_font_spaces)
    large_font = True

    text = command_input.arguments[0]
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

    return runes
