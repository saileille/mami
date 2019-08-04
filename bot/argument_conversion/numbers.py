"""Number-related argument conversion."""
from bot.misc import embed_messages


async def valid_no_of_dice(argument, context):
    """
    Check that the argument is within valid number of dice.

    If argument is valid, return it converted to an integer.
    """
    int_range = [1, context.max_dice]
    number = await integer_in_range(argument, context, int_range, verbose=False)

    if number is None:
        custom_msg = await context.language.get_text(
            "not_integer_in_range", {"min_value": 1, "max_value": context.max_dice})
        await embed_messages.invalid_argument(context, argument, custom_msg)

    return number


async def integer(argument, context, verbose=True):
    """Convert the argument to an integer."""
    number = None
    try:
        number = int(argument)
    except ValueError:
        if verbose:
            custom_msg = await context.language.get_text("not_integer")
            await embed_messages.invalid_argument(context, argument, custom_msg)

    return number


async def to_float(argument, context, verbose=True):
    """Convert the argument to a float."""
    number = None
    try:
        number = float(argument)
    except ValueError:
        if verbose:
            custom_msg = await context.language.get_text("not_float")
            await embed_messages.invalid_argument(context, argument, custom_msg)

    return number


async def positive_float(argument, context):
    """Convert argument to a float that is higher than 0."""
    return await float_in_range(argument, context, [0, None])


async def integer_in_range(argument, context, int_range, verbose=True):
    """
    Check that the argument is within a certain range. Helper function.

    If argument is valid, return it converted to an integer.
    The upper or lower limit can be emitted from the range with None as value.
    """
    number = await integer(argument, context, verbose=False)

    if number is not None:
        if None not in int_range:
            int_range.sort()

        below_min_range = int_range[0] is not None and number < int_range[0]
        above_max_range = int_range[1] is not None and number > int_range[1]

        if below_min_range or above_max_range:
            number = None

    if number is None and verbose:
        custom_msg = None

        if int_range[1] is None:
            custom_msg = await context.language.get_text(
                "integer_below_min_value", {"value": int_range[0]})
        elif int_range[0] is None:
            custom_msg = await context.language.get_text(
                "integer_above_max_value", {"value": int_range[1]})
        else:
            custom_msg = await context.language.get_text(
                "not_integer_in_range",
                {"min_value": int_range[0], "max_value": int_range[1]})

        await embed_messages.invalid_argument(context, argument, custom_msg)

    return number


async def float_in_range(argument, context, float_range, verbose=True):
    """
    Check that the argument is within a certain range. Helper function.

    If argument is valid, return it converted to a float.
    The upper or lower limit can be emitted from the range with None as value.
    """
    number = await to_float(argument, context, verbose=False)

    if None not in float_range:
        float_range.sort()

    below_min_range = float_range[0] is not None and number < float_range[0]
    above_max_range = float_range[1] is not None and number > float_range[1]
    if number is not None and (below_min_range or above_max_range):
        number = None

    if number is None and verbose:
        custom_msg = None

        if float_range[1] is None:
            custom_msg = await context.language.get_text(
                "float_below_min_value", {"value": float_range[0]})
        elif float_range[0] is None:
            custom_msg = await context.language.get_text(
                "float_above_max_value", {"value": float_range[1]})
        else:
            custom_msg = await context.language.get_text(
                "not_float_in_range",
                {"min_value": float_range[0], "max_value": float_range[1]})

        await embed_messages.invalid_argument(context, argument, custom_msg)

    return number
