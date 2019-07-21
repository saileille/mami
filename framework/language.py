"""Contains language data."""
import json
import os

from bot.data import default_values
from bot.data import definitions
from framework import custom_json


class Language():
    """Contains language data."""

    special_files = ["commands.json", "languages.json", "meta.json", "permissions.json",
                     "units.json"]

    def __init__(self, obj_id):
        """Initialise object."""
        self.obj_id = obj_id

        self.flag_codes = []
        self.translators = []
        self.keys = {}
        self.languages = {}
        self.permission_names = {}
        self.unit_data = {}

    @property
    def flag_emojis(self):
        """Get the flag emojis of the language."""
        string = ""
        for code in self.flag_codes:
            if string != "":
                string += "/"

            string += code

        return string

    @property
    def directory(self):
        """Get the absolute path of the language directory."""
        return os.path.join(definitions.ROOT_DIR, "languages", self.obj_id)

    def add_keys_from_path(self, path):
        """Add language keys."""
        file_keys = None
        with open(path, "r", encoding="utf-8") as file:
            file_keys = None
            try:
                file_keys = json.load(file)
            except json.decoder.JSONDecodeError:
                file_keys = {}

        for key in file_keys:
            if key in self.keys:
                print("Key '" + key + "' already exists in language '" + self.obj_id + "'!")
            else:
                if self.obj_id == default_values.LANGUAGE_ID:
                    definitions.DEFAULT_LANGUAGE_KEY_LOCATIONS[key] = path

                self.keys[key] = file_keys[key]

    def add_languages(self, path):
        """Add languages."""
        file_keys = None
        with open(path, "r", encoding="utf-8") as file:
            file_keys = None
            try:
                file_keys = json.load(file)
            except json.decoder.JSONDecodeError:
                file_keys = {}

        self.languages = file_keys

    def add_meta(self, path):
        """Add the metadata."""
        data = None
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {
                    "flag_codes": [], "translators": []}

        if "flag_codes" in data:
            for code in data["flag_codes"]:
                self.flag_codes.append(":flag_{code}:".format(code=code))

        if "translators" in data:
            for name in data["translators"]:
                self.translators.append(name)

    def add_permission_names(self, path):
        """Add the permission names."""
        data = None
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}

        self.permission_names = data

    def add_units(self, path):
        """Add the unit names."""
        data = None
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}

        self.unit_data = data

    def synchronise_keys(self):
        """Make the language only have those keys which are in the default language."""
        default_language = definitions.LANGUAGES[default_values.LANGUAGE_ID]

        self.delete_obsolete_keys(default_language)
        self.add_new_keys(default_language)

    def delete_obsolete_keys(self, default_language):
        """Remove keys that no longer exist in the default language."""
        obsolete_keys = []
        for key in self.keys:
            if key not in default_language.keys:
                obsolete_keys.append(key)

        for root, dirs, files in os.walk(self.directory):
            for name in files:
                full_dir = os.path.join(root, name)
                relative_dir = full_dir.replace(self.directory, "")
                if relative_dir[0] == "\\":
                    relative_dir = relative_dir[1:]

                if relative_dir not in Language.special_files:
                    key_dict = custom_json.load(full_dir)

                    found_obsolete_key = False
                    for key in obsolete_keys:
                        if key in key_dict:
                            found_obsolete_key = True
                            del key_dict[key]

                    if found_obsolete_key:
                        custom_json.save(key_dict, full_dir, compact=False)

                elif relative_dir != "commands.json":
                    obsolete_special_keys = []
                    lang_dict = custom_json.load(full_dir)
                    default_dict = custom_json.load(
                        os.path.join(default_language.directory, name))

                    for key in lang_dict:
                        if key not in default_dict:
                            obsolete_special_keys.append(key)

                    for key in obsolete_special_keys:
                        del lang_dict[key]

                    if obsolete_special_keys:
                        custom_json.save(lang_dict, full_dir, compact=False)

    def add_new_keys(self, default_language):
        """Add new language keys from the default language."""
        new_keys = []
        for key in default_language.keys:
            if key not in self.keys:
                new_keys.append(key)

        for key in new_keys:
            directory_list = definitions.DEFAULT_LANGUAGE_KEY_LOCATIONS[key].split("\\")
            id_index = directory_list.index(default_values.LANGUAGE_ID)
            directory_list[id_index] = self.obj_id
            directory_list[-1] = "_NEW_" + directory_list[-1]
            directory = "\\".join(directory_list)

            key_dict = custom_json.load(directory)
            if key_dict is None:
                key_dict = {}

            key_dict[key] = default_language.keys[key]
            custom_json.save(key_dict, directory, compact=False)

        for special_file in Language.special_files:
            if special_file == "commands.json":
                continue

            lang_dict = custom_json.load(os.path.join(self.directory, special_file))
            if lang_dict is None:
                lang_dict = {}

            default_dict = custom_json.load(
                os.path.join(default_language.directory, special_file))
            new_lang_dict = custom_json.load(
                os.path.join(self.directory, "_NEW_" + special_file))

            if new_lang_dict is None:
                new_lang_dict = {}

            changed_dict = False
            for key in default_dict:
                if key not in lang_dict and key not in new_lang_dict:
                    changed_dict = True
                    new_lang_dict[key] = default_dict[key]

            if changed_dict:
                custom_json.save(
                    new_lang_dict, os.path.join(self.directory, "_NEW_" + special_file),
                    compact=False)

    async def get_text(self, key, variables=None):
        """
        Get localised text from the language.

        If text is not found, return the key.
        """
        if variables is None:
            variables = {}

        if key in self.keys:
            return self.keys[key].format(**variables)

        return key

    async def get_language(self, key):
        """
        Get localised language name from a language key.

        If language is not found, return the key.
        """
        if key in self.languages:
            return self.languages[key]

        return key

    async def format_number(self, number, decimal_rules=""):
        """Format number so it has localised thousands separator and decimal symbol."""
        separator = await self.get_text("thousands_separator")
        decimal = await self.get_text("decimal_symbol")

        return format(
            number, "," + decimal_rules).replace(
                ",", "X").replace(
                    ".", decimal).replace(
                        "X", separator)

    async def get_string_list(self, str_list):
        """Get a localised string representation of a list."""
        string = ""
        for i, item in enumerate(str_list):
            if i > 0:
                if i + 1 == len(str_list):
                    string += await self.get_text("last_list_separator")
                else:
                    string += await self.get_text("normal_list_separator")

            string += item

        return string

    async def get_default_unit_symbol(self, unit_key):
        """
        Get the default localised symbol of a unit.

        Get the first symbol defined if there is one.
        If there is no symbol, get the first defined name.
        """
        symbols_and_names = self.unit_data[unit_key]
        default_symbol = None
        if symbols_and_names["symbols"]:
            default_symbol = symbols_and_names["symbols"][0]
        else:
            default_symbol = symbols_and_names["names"][0]

        return default_symbol
