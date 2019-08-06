"""String-related aid functions."""


def modify_filepath(path, file_prefix, *replacements):
    """
    Replace parts of a filepath and add prefix to the filename.

    Used for making special language files.
    """
    directory_list = path.split("\\")

    for replacement in replacements:
        id_index = directory_list.index(replacement["original"])
        directory_list[id_index] = replacement["new"]

    directory_list[-1] = file_prefix + directory_list[-1]
    return "\\".join(directory_list)


async def get_yes_no_emojis(boolean):
    """Get ✅ if True, ❎ if False."""
    if boolean:
        return "✅"

    return "❎"
