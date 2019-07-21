"""Date-related functions."""
import calendar
import datetime


async def get_time_difference_string(context, past):
    """Get a string represenation of a time difference."""
    now = datetime.datetime.utcnow()

    time = {
        "years": now.year - past.year,
        "months": now.month - past.month,
        "days": now.day - past.day,
        "hours": now.hour - past.hour,
        "minutes": now.minute - past.minute,
        "seconds": now.second - past.second,
        "microseconds": now.microsecond - past.microsecond}

    while time["microseconds"] < 0:
        time["seconds"] -= 1
        time["microseconds"] += 1000000

    while time["seconds"] < 0:
        time["minutes"] -= 1
        time["seconds"] += 60

    while time["minutes"] < 0:
        time["hours"] -= 1
        time["minutes"] += 60

    while time["hours"] < 0:
        time["days"] -= 1
        time["hours"] += 24

    while time["days"] < 0:
        month_data = calendar.monthrange(past.year, past.month)
        time["months"] -= 1
        time["days"] += month_data[1]

    while time["months"] < 0:
        time["years"] -= 1
        time["months"] += 12

    time["weeks"], time["days"] = divmod(time["days"], 7)

    time_list = []
    for unit in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]:
        if time[unit] == 1:
            time_list.append(await context.language.get_text(
                "time_" + unit + "_singular", {unit: time[unit]}))
        elif time[unit] != 0:
            time_list.append(await context.language.get_text(
                "time_" + unit + "_plural", {unit: time[unit]}))

    return await context.language.get_string_list(time_list)
