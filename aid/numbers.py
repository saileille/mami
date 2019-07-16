"""Aiding functions related to numbers."""


async def get_percentage(value, divider):
    """
    Get a percentage value.

    The function accounts for the possibility of divider being 0, in which case the
    percentage is 0 as well.
    """
    percentage = None
    if divider == 0:
        percentage = 0.0
    else:
        percentage = float(value) / float(divider) * 100

    return percentage


async def convert(amount, base_rate, target_rate, base_zero_point=0, target_zero_point=0):
    """Convert between units."""
    target_amount = amount
    zero_difference = target_zero_point - base_zero_point
    conversion_rate = float(target_rate) / float(base_rate)

    if zero_difference < 0:
        target_amount += zero_difference

    target_amount *= conversion_rate

    if zero_difference > 0:
        target_amount += zero_difference

    return target_amount
