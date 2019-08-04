"""
Automatic unit conversion.

Useful regex checks:
https://ja.wikipedia.org/wiki/%E6%B7%B1%E8%A6%8B%E7%9C%9F
http://ja.wikipedia.org/wiki/%E6%B7%B1%E8%A6%8B%E7%9C%9F
ftp://ja.wikipedia.org/wiki/%E6%B7%B1%E8%A6%8B%E7%9C%9F
www.9anime.to
9anime.to
www.9anime
(https://ja.wikipedia.org/wiki/%E6%B7%B1%E8%A6%8B%E7%9C%9F)
(http://ja.wikipedia.org/wiki/%E6%B7%B1%E8%A6%8B%E7%9C%9F)
(ftp://ja.wikipedia.org/wiki/%E6%B7%B1%E8%A6%8B%E7%9C%9F)
(www.9anime.to)
(9anime.to)
(www.9anime)

"5km"
!!!5 kilometres!!!
a5 km
5 km2
a!5km^2
1"5km"
5  km

".5km"
!!!.5 kilometres!!!
a.5 km
.5 km2
a!.5km^2
1".5km"
.5  km

"0.5km"
!!!0.5 kilometres!!!
a0.5 km
55.5km
0.5 km2
a!0.5km^2
1"0.5km"
0.5  km

"5.km"
!!!5. kilometres!!!
a5. km
5. km2
a!5.km^2
1"5.km"
5.  km
"""
import re

from aid import numbers
from bot.data import default_values
from framework import embeds

conversion_dict = {
    "mile": ["kilometre"],
    "kilometre": ["mile"],
    "metre": ["foot"],
    "yard": ["metre"],
    "foot": ["metre"],
    "inch": ["centimetre"],
    "centimetre": ["inch"],
    "pica": ["centimetre"],
    "millimetre": ["inch"],
    "acre": ["square_metre"],
    "square_metre": ["acre"],
    "celsius": ["fahrenheit"],
    "fahrenheit": ["celsius"],
    "imperial_gallon": ["litre", "us_gallon"],
    "us_gallon": ["litre", "imperial_gallon"],
    "litre": ["us_gallon", "imperial_gallon"],
    "imperial_cup": ["desilitre"],
    "us_legal_cup": ["desilitre"],
    "desilitre": ["us_legal_cup"],
    "us_fluid_ounce": ["millilitre", "imperial_fluid_ounce"],
    "imperial_fluid_ounce": ["millilitre", "us_fluid_ounce"],
    "millilitre": ["us_fluid_ounce"],
    "stone": ["kilogram", "pound"],
    "kilogram": ["pound", "stone"],
    "pound": ["kilogram", "stone"],
    "ounce": ["gram"],
    "gram": ["ounce"],
    "milligram": ["ounce"]}


async def detect_unit_mention(context):
    """
    Detect if there is a conversion to be made.

    First processes message so that all hyperlinks are eliminated.
    """
    message = await remove_hyperlinks(context.message.content)
    unit_matches = await get_unit_matches(context, message)

    has_info_reaction = False
    for reaction in context.message.reactions:
        if reaction.emoji == "ℹ" and reaction.me:
            has_info_reaction = True
            break

    if unit_matches and not has_info_reaction:
        await context.message.add_reaction("ℹ")
    elif not unit_matches and has_info_reaction:
        await context.message.remove_reaction("ℹ", context.message.guild.me)


async def remove_hyperlinks(message):
    """Go through the message and return a new message string without them."""
    return re.sub(r"\S*(?:(?:https?|ftp):\/\/)\S*", "[url]", message)


async def get_unit_matches(context, message):
    """Get all unit matches from a message."""
    unit_regex = r"(?<!\w)((?:\d*\.\d+)|\d+)[ -]?((?:(?:[^\d\s\.]+\S*) ?)+)"
    us_height_regex = r"\b(\d+)['′] ?(\d+)[\"″](?!\w)"

    matches = re.findall(unit_regex, message)
    us_height_matches = re.findall(us_height_regex, message)

    processed_matches = []
    for match in matches:
        # Cannot disable 0-conversions here because temperatures are a thing.
        await process_match(context, match, processed_matches)

    for match in us_height_matches:
        processed_matches.append([float(match[0]), float(match[1])])

    return processed_matches


async def process_match(context, match, processed_matches):
    """Evaluate a normal match."""
    for key in conversion_dict:
        unit = context.language.unit_data[key]
        found_match = False
        for symbol in unit["symbols"]:
            match_unit_name = match[1].split(" ")
            inspected_unit_name = symbol.split(" ")

            if await validate_unit_name(match_unit_name, inspected_unit_name):
                processed_matches.append([float(match[0]), key])
                found_match = True
                break

        for name in unit["names"]:
            match_unit_name = match[1].lower().split(" ")
            inspected_unit_name = name.lower().split(" ")

            if await validate_unit_name(match_unit_name, inspected_unit_name):
                processed_matches.append([float(match[0]), key])
                found_match = True
                break

        if found_match:
            break


async def validate_unit_name(match_unit_name, inspected_unit_name):
    """Validate the unit name."""
    not_letter = r"\W"
    for i, inspected_name_part in enumerate(inspected_unit_name):
        """
        Ignoring exception in on_message
        Traceback (most recent call last):
          File "C:\Program Files\Python37\lib\site-packages\discord\client.py", line 251, in _run_event
            await coro(*args, **kwargs)
          File "E:\Tiedostot\DiscordBot\Mami\framework\client.py", line 39, in on_message
            await Client.handle_message(message)
          File "E:\Tiedostot\DiscordBot\Mami\framework\client.py", line 71, in handle_message
            await auto_convert.detect_unit_mention(context)
          File "E:\Tiedostot\DiscordBot\Mami\bot\mechanics\auto_convert.py", line 66, in detect_unit_mention
            unit_matches = await get_unit_matches(context, message)
          File "E:\Tiedostot\DiscordBot\Mami\bot\mechanics\auto_convert.py", line 96, in get_unit_matches
            await process_match(context, match, processed_matches)
          File "E:\Tiedostot\DiscordBot\Mami\bot\mechanics\auto_convert.py", line 121, in process_match
            if await validate_unit_name(match_unit_name, inspected_unit_name):
          File "E:\Tiedostot\DiscordBot\Mami\bot\mechanics\auto_convert.py", line 134, in validate_unit_name
            match_name_part = match_unit_name[i].strip()
        IndexError: list index out of range
        """
        match_name_part = match_unit_name[i].strip()
        inspected_name_part = inspected_name_part.strip()

        if match_name_part != inspected_name_part:
            while match_name_part and re.match(not_letter, match_name_part[-1]):
                match_name_part = match_name_part[:-1]
                if match_name_part == inspected_name_part:
                    break
            else:
                return False

    return True


async def send_conversion(context, user_id=None):
    """Convert the found units and sends them to the channel."""
    message = await remove_hyperlinks(context.message.content)
    unit_matches = await get_unit_matches(context, message)

    if not unit_matches:
        return

    for reaction in context.message.reactions:
        if reaction.emoji == "ℹ":
            async for user in reaction.users():
                await reaction.remove(user)

    msg = ""

    for match in unit_matches:
        if msg != "":
            msg += "\n"

        if match[1] == "centimetre" and match[0] > 100:
            msg += await convert_to_us_height(context, match)
        elif isinstance(match[1], str):
            msg += await convert_normal(context, match)
        elif isinstance(match[1], float):
            msg += await convert_from_us_height(context, match)

    message = embeds.PaginatedEmbed(
        await context.language.get_text("auto_conversion_title"))

    member = context.message.guild.get_member(user_id)
    thumbnail = "default"
    if member:
        message.embed.title = await context.language.get_text(
            "auto_conversion_request", {"name": member.display_name})
        thumbnail = member.avatar_url

    message.embed.description = msg
    await message.send(context, thumbnail=thumbnail)


async def convert_normal(context, match):
    """Calculate normal conversions."""
    base = {
        "amount": match[0],
        "key": match[1],
        "rate": 0,
        "zero_point": 0}

    category = None
    for key, unit_category in default_values.UNIT_RATES.items():
        if base["key"] in unit_category:
            category = default_values.UNIT_RATES[key]
            break

    targets = []
    for target_key in conversion_dict[base["key"]]:
        targets.append(
            {"amount": base["amount"],
             "key": target_key,
             "rate": 0,
             "zero_point": 0})

    if isinstance(category[base["key"]], dict):
        base["rate"] = category[base["key"]]["rate"]
        base["zero_point"] = category[base["key"]]["zero_point"]

        for target in targets:
            target["rate"] = category[target["key"]]["rate"]
            target["zero_point"] = category[target["key"]]["zero_point"]

    else:
        base["rate"] = category[base["key"]]
        for target in targets:
            target["rate"] = category[target["key"]]

    base["unit"] = await context.language.get_default_unit_symbol(base["key"])
    base["formatted_amount"] = await context.language.format_number(base["amount"])
    base_unit_and_amount = await context.language.get_text(
        "unit_representation",
        {"unit_amount": base["formatted_amount"], "unit_name": base["unit"]})

    target_conv_list = []
    for target in targets:
        target["unit"] = await context.language.get_default_unit_symbol(target["key"])
        target["amount"] = await numbers.convert(
            base["amount"], base["rate"], target["rate"], base["zero_point"],
            target["zero_point"])

        target["formatted_amount"] = await context.language.format_number(
            target["amount"], decimal_rules=".3f")

        target_conv_list.append(await context.language.get_text(
            "unit_representation",
            {"unit_amount": target["formatted_amount"], "unit_name": target["unit"]}))

    target_conversions = await context.language.get_string_list(target_conv_list)

    return await context.language.get_text(
        "unit_conversion",
        {"unit_and_amount": base_unit_and_amount, "conversion_list": target_conversions})


async def convert_from_us_height(context, match):
    """Calculate the U.S. height."""
    height_text = "{match[0]:.0f}′ {match[1]:.0f}″".format(match=match)

    cm_rate = default_values.UNIT_RATES["length"]["centimetre"]
    ft_rate = default_values.UNIT_RATES["length"]["foot"]
    in_rate = default_values.UNIT_RATES["length"]["inch"]

    centimetres = await numbers.convert(match[0], ft_rate, cm_rate)
    centimetres += await numbers.convert(match[1], in_rate, cm_rate)

    cm_text = await context.language.get_text(
        "unit_representation",
        {"unit_amount": await context.language.format_number(
            centimetres, decimal_rules=".2f"),
         "unit_name": await context.language.get_default_unit_symbol("centimetre")})

    return await context.language.get_text(
        "unit_conversion", {"unit_and_amount": height_text, "conversion_list": cm_text})


async def convert_to_us_height(context, match):
    """
    Convert to U.S. height.

    Fires if converting more than 100 centimetres.
    """
    cm_rate = default_values.UNIT_RATES["length"]["centimetre"]
    in_rate = default_values.UNIT_RATES["length"]["inch"]

    inches = await numbers.convert(match[0], cm_rate, in_rate)
    feet, inches = divmod(inches, 12)

    feet_and_inches = "{feet:.0f}′ {inches:.0f}″".format(feet=feet, inches=inches)
    centimetres = await context.language.get_text(
        "unit_representation",
        {"unit_amount": await context.language.format_number(match[0]),
         "unit_name": await context.language.get_default_unit_symbol("centimetre")})

    return await context.language.get_text(
        "unit_conversion",
        {"unit_and_amount": feet_and_inches, "conversion_list": centimetres})
