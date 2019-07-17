"""Dice-related commands."""
import random
import discord

from aid import lists
from aid import numbers
from framework import embeds


async def throw(context, command_input):
    """Throw the dice."""
    no_of_dice = command_input.arguments[0]
    dice_range = command_input.arguments[1:]
    dice_range.sort()

    dice_throws = []
    dice_results = []
    while len(dice_throws) < no_of_dice:
        dice_throw = random.randint(dice_range[0], dice_range[1])
        dice_throws.append(dice_throw)
        dice_results.append(":game_die: " + await context.language.format_number(
            dice_throw))

    dice_total = sum(dice_throws)
    min_total = dice_range[0] * no_of_dice
    max_total = dice_range[1] * no_of_dice
    percentage = await numbers.get_percentage(
        dice_total - min_total, max_total - min_total)

    formatted_percentage = await context.get_language_text(
        "percentage",
        {"number": await context.language.format_number(percentage, decimal_rules=".2f")})

    column_strings = None
    thumbnail = None
    if context.desktop_ui:
        column_strings = await lists.divide_into_columns(dice_results, 3)
    else:
        column_strings = await lists.divide_into_columns(dice_results, 1)
        thumbnail = "default"

    embed = discord.Embed()
    embed.description = await context.get_language_text("throw_dice_desc")

    for column in column_strings:
        embed.add_field(
            name=await context.get_language_text("dice_results_title"),
            value=column)

    embed.add_field(
        name=await context.get_language_text("dice_results_analysis_title"),
        value=await context.get_language_text(
            "dice_results_analysis_content",
            {"dice_total": await context.language.format_number(dice_total),
             "min_total": await context.language.format_number(min_total),
             "max_total": await context.language.format_number(max_total),
             "percentage": formatted_percentage}),
        inline=False)

    await embeds.send(
        context, await context.get_language_text("throw_dice_title"), embed,
        thumbnail=thumbnail)
