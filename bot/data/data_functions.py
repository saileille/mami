"""Contains some functions related to handling data."""
from bot.data import definitions


async def get_command_from_id_list(id_list):
    """
    Get a Command object from a given ID list.

    The ID list represents the path to the command. The function presumes
    that all IDs are valid and that the list forms a valid command path.
    """
    command = definitions.COMMANDS
    for cmd_id in id_list:
        for sub_command in command.sub_commands:
            if cmd_id == sub_command.obj_id:
                command = sub_command
                break

    return command


async def get_id_path_from_command_name(name, context):
    """Get the ID path from a command name written in any language."""
    name_list = name.split(".")
    command = definitions.COMMANDS
    id_path = []

    for name_part in name_list:
        for sub_command in command.sub_commands.values():
            if name_part in sub_command.localisation[context.language_id]["names"]:
                id_path.append(sub_command.obj_id)
                command = sub_command
                break
        else:
            return None

    return id_path
