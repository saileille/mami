"""Dice-related commands."""
import random

from aid import numbers
from framework import embeds


async def throw(context, arguments):
    """Throw the dice."""
    no_of_dice = arguments[0]
    dice_range = arguments[1:]
    dice_range.sort()

    dice_throws = []
    dice_results = []
    while len(dice_throws) < no_of_dice:
        dice_throw = random.randint(dice_range[0], dice_range[1])
        dice_throws.append(dice_throw)
        dice_results.append("🎲 " + await context.language.format_number(
            dice_throw))

    dice_total = sum(dice_throws)
    min_total = dice_range[0] * no_of_dice
    max_total = dice_range[1] * no_of_dice
    percentage = await numbers.get_percentage(
        dice_total - min_total, max_total - min_total)

    formatted_percentage = await context.language.get_text(
        "percentage",
        {"number": await context.language.format_number(percentage, decimal_rules=".2f")})

    thumbnail = "default"
    column_amount = 1
    if context.desktop_ui:
        column_amount = 3
        thumbnail = None

    message = embeds.PaginatedEmbed(
        await context.language.get_text("throw_dice_title"),
        embeds.EmbedFieldCollection(
            dice_results, await context.language.get_text("dice_results_title"),
            column_amount),
        embeds.EmbedFieldCollection(
            await context.language.get_text(
                "dice_results_analysis_content",
                {"dice_total": await context.language.format_number(dice_total),
                 "min_total": await context.language.format_number(min_total),
                 "max_total": await context.language.format_number(max_total),
                 "percentage": formatted_percentage}),
            await context.language.get_text("dice_results_analysis_title")))

    message.embed.description = await context.language.get_text(
        "throw_dice_desc", {"user_mention": context.message.author.mention})

    await message.send(context, thumbnail=thumbnail)
    return True
