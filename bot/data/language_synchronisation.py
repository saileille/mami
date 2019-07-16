"""Functions to synchronise the language-data with up-to-date information."""
import os

from bot.data import default_values
from bot.data import definitions
from framework import custom_json


def synchronise():
    """Synchronise all languages."""
    synchronise_commands()
    synchronise_keys()


def synchronise_commands():
    """Make command language data synchronised with existing commands."""
    for language in definitions.LANGUAGES.values():
        command_file_dir = os.path.join(language.directory, "commands.json")
        language_command_dict = custom_json.load(command_file_dir)

        if synchronise_command_layer(language_command_dict, language.obj_id):
            custom_json.save(language_command_dict, command_file_dir, compact=False)


def synchronise_command_layer(language_dict, language_id, command_dict=None):
    """
    Make a layer of command language data synchronised with existing commands.

    Return a boolean whether the command or its sub-commands had new data.
    """
    if command_dict is None:
        command_dict = definitions.COMMANDS.sub_commands

    changed_language_dict = delete_obsolete_command_items(language_dict, command_dict)

    for key, command in command_dict.items():
        if key not in language_dict:
            language_data = command.create_language_data(language_id)
            if language_data:
                changed_language_dict = True
                language_dict[key] = language_data

        elif command.sub_commands:
            changed_sub_command = synchronise_command_layer(
                language_dict[key]["sub_commands"], language_id, command.sub_commands)

            if not changed_language_dict and changed_sub_command:
                changed_language_dict = changed_sub_command

    return changed_language_dict


def delete_obsolete_command_items(language_dict, command_dict):
    """
    Delete all language data of non-existent commands.

    Return a boolean whether any information was changed.
    """
    delete_keys = []
    for key in language_dict:
        if key not in command_dict:
            delete_keys.append(key)

    for key in delete_keys:
        del language_dict[key]

    return bool(delete_keys)


def synchronise_keys():
    """Synchronise all keys of different languages."""
    for key, language in definitions.LANGUAGES.items():
        if key != default_values.LANGUAGE_ID:
            language.synchronise_keys()
