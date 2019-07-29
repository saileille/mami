"""Functions to synchronise the language-data with up-to-date information."""
import os
import shutil
from distutils import dir_util

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
        if language_command_dict is None:
            language_command_dict = {}

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


def get_changed_keys():
    """Get the language keys that have been changed since last start."""
    changed_keys = {"default": {}, "languages": {}, "permissions": {}, "units": {}}

    cache = definitions.CACHE_LANGUAGE
    if cache is None:
        return changed_keys

    default = definitions.LANGUAGES[default_values.LANGUAGE_ID]

    for key, value in default.keys.items():
        if key in cache.keys and value != cache.keys[key]:
            changed_keys["default"][key] = value

    for key, value in default.languages.items():
        if key in cache.languages and value != cache.languages[key]:
            changed_keys["languages"][key] = value

    for key, value in default.permission_names.items():
        if key in cache.permission_names and value != cache.permission_names[key]:
            changed_keys["permissions"][key] = value

    for key, value in default.unit_data.items():
        if key in cache.unit_data and value != cache.unit_data[key]:
            changed_keys["units"][key] = value

    return changed_keys


def synchronise_keys():
    """Synchronise all keys of different languages."""
    changed_keys = get_changed_keys()

    for key, language in definitions.LANGUAGES.items():
        if key != default_values.LANGUAGE_ID:
            language.synchronise_keys(changed_keys)

    default_language = definitions.LANGUAGES[default_values.LANGUAGE_ID]
    cache_language = definitions.CACHE_LANGUAGE

    if default_language != cache_language:
        update_cache()


def update_cache():
    """Update the cache language for the next time."""
    language_dir = os.path.join(definitions.ROOT_DIR, "languages")
    cache_folder = os.path.join(language_dir, "cache")
    default_folder = os.path.join(language_dir, default_values.LANGUAGE_ID)

    for root, dirs, files in os.walk(cache_folder):
        for name in files:
            full_dir = os.path.join(root, name)
            os.remove(full_dir)

        for folder in dirs:
            full_dir = os.path.join(root, folder)
            shutil.rmtree(full_dir)

    dir_util.copy_tree(default_folder, cache_folder)
    print("Cache language updated.")
