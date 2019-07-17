"""Aiding functions related to lists."""


async def divide_into_columns(content_list, column_amount, horizontal=True):
    """Divide string list into equally sized parts for inline column placement."""
    if horizontal:
        return await divide_into_horizontal_columns(content_list, column_amount)

    return await divide_into_vertical_columns(content_list, column_amount)


async def divide_into_vertical_columns(content_list, column_amount):
    """
    Divide string list into equally sized parts for inline column placement.

    The order goes from column to column (vertically).
    """
    base_column_size, extras = divmod(len(content_list), column_amount)

    column_strings = []
    content_list_index = 0
    for i in range(column_amount):
        column_size = base_column_size
        if extras > i:
            column_size += 1

        for j in range(column_size):
            content = content_list[content_list_index]
            if len(column_strings) <= i:
                column_strings.append(content)
            else:
                column_strings[i] += "\n" + content

            content_list_index += 1

    return column_strings


async def divide_into_horizontal_columns(content_list, column_amount):
    """
    Divide string list into equally sized parts for inline column placement.

    The order goes from row to row (horizontally).
    """
    column_strings = []
    for i, content in enumerate(content_list):
        column_index = i % column_amount
        if len(column_strings) < column_amount:
            column_strings.append(content)
        else:
            column_strings[column_index] += "\n" + content

    return column_strings
