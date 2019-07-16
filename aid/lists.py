"""Aiding functions related to lists."""


async def divide_into_columns(content_list, columns):
    """Divides string list into equally sized parts for inline column placement."""
    base_column_size, extras = divmod(len(content_list), columns)

    column_strings = []
    content_list_index = 0
    for i in range(columns):
        column_size = base_column_size
        if extras > i:
            column_size += 1

        for j in range(column_size):
            if len(column_strings) <= i:
                column_strings.append("")
            else:
                column_strings[i] += "\n"

            column_strings[i] += content_list[content_list_index]
            content_list_index += 1

    return column_strings
