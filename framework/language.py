"""Contains language data."""
import json
import os

from aid import strings
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

    def __eq__(self, compare):
        """
        See if the two languages are identical.

        Does not take commands or ID into account.
        """
        if not (isinstance(compare, Language) and
                len(self.flag_codes) == len(compare.flag_codes) and
                len(self.translators) == len(compare.translators) and
                len(self.keys.keys()) == len(compare.keys.keys()) and
                len(self.languages.keys()) == len(compare.languages.keys()) and
                len(self.permission_names.keys()) == len(compare.permission_names.keys()) and
                len(self.unit_data.keys()) == len(compare.unit_data.keys())):
            return False

        for i, flag_code in enumerate(self.flag_codes):
            if compare.flag_codes[i] != flag_code:
                return False

        for i, translator in enumerate(self.translators):
            if compare.translators[i] != translator:
                return False

        for key, value in self.keys.items():
            if key not in compare.keys or compare.keys[key] != value:
                return False

        for key, value in self.languages.items():
            if key not in compare.languages or compare.languages[key] != value:
                return False

        for key, value in self.permission_names.items():
            if (key not in compare.permission_names or
                compare.permission_names[key] != value):
                return False

        for key, value in self.unit_data.items():
            if key not in compare.unit_data or compare.unit_data[key] != value:
                return False

        return True

    @property
    def flag_emoji(self):
        """Get a flag emoji string of the language."""
        if self.flag_codes:
            return self.flag_codes[0]
        else:
            return None

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
                self.flag_codes.append(code)

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

    def synchronise_keys(self, changed_keys):
        """Make the language only have those keys which are in the default language."""
        self.delete_obsolete_keys()
        self.add_new_keys()
        self.reveal_changed_keys(changed_keys)

    def delete_obsolete_keys(self):
        """Remove keys that no longer exist in the default language."""
        default_language = definitions.LANGUAGES[default_values.LANGUAGE_ID]

        for root, dirs, files in os.walk(self.directory):
            for name in files:
                full_dir = os.path.join(root, name)
                relative_dir = full_dir.replace(self.directory, "")

                if relative_dir[0] == "\\":
                    relative_dir = relative_dir[1:]

                file_dict, changed_dict, changed_dir, new_dict, new_dir = get_files(
                    full_dir)

                found_obsolete_key = False
                found_changed_obsolete_key = False
                found_new_obsolete_key = False

                if relative_dir not in Language.special_files:
                    for key in list(file_dict.keys()):
                        if key not in default_language.keys:
                            found_obsolete_key = True
                            del file_dict[key]

                            if key in changed_dict:
                                found_changed_obsolete_key = True
                                del changed_dict[key]

                    for key in list(new_dict.keys()):
                        if key not in default_language.keys:
                            found_new_obsolete_key = True
                            del new_dict[key]

                elif relative_dir != "commands.json":
                    default_dict = custom_json.load(
                        os.path.join(default_language.directory, name))

                    for key in list(file_dict.keys()):
                        if key not in default_dict:
                            del file_dict[key]
                            found_obsolete_key = True

                            if key in changed_dict:
                                del changed_dict[key]
                                found_changed_obsolete_key = True

                    for key in list(new_dict.keys()):
                        if key not in default_dict:
                            del new_dict[key]
                            found_new_obsolete_key = True

                if found_obsolete_key:
                    custom_json.save(file_dict, full_dir, compact=False)

                if found_changed_obsolete_key:
                    custom_json.save(changed_dict, changed_dir, compact=False)

                if found_new_obsolete_key:
                    custom_json.save(new_dict, new_dir, compact=False)

    def add_new_keys(self):
        """Add new language keys from the default language."""
        default_language = definitions.LANGUAGES[default_values.LANGUAGE_ID]

        new_keys = []
        for key in default_language.keys:
            if key not in self.keys:
                new_keys.append(key)

        for key in new_keys:
            directory = strings.modify_filepath(
                definitions.DEFAULT_LANGUAGE_KEY_LOCATIONS[key], "_NEW_",
                {"original": default_values.LANGUAGE_ID, "new": self.obj_id})

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

    def reveal_changed_keys(self, changed_keys):
        """Let translators know of keys that have been changed."""
        for root, dirs, files in os.walk(self.directory):
            for name in files:
                if name.startswith("_NEW_") or name.startswith("_CHANGED_"):
                    continue

                full_dir = os.path.join(root, name)
                relative_dir = full_dir.replace(self.directory, "")

                if relative_dir[0] == "\\":
                    relative_dir = relative_dir[1:]

                file_dict, changed_dict, changed_dir, new_dict, new_dir = get_files(
                    full_dir)

                has_changed_keys = False
                has_new_changed_keys = False

                if relative_dir not in Language.special_files:
                    for key, value in changed_keys["default"].items():
                        if key in file_dict:
                            changed_dict[key] = value
                            has_changed_keys = True
                        elif key in new_dict:
                            new_dict[key] = value
                            has_new_changed_keys = True

                elif relative_dir == "languages.json" and changed_keys["languages"]:
                    for key, value in changed_keys["languages"].items():
                        if key in file_dict:
                            changed_dict[key] = value
                            has_changed_keys = True
                        elif key in new_dict:
                            new_dict[key] = value
                            has_new_changed_keys = True

                elif relative_dir == "permissions.json" and changed_keys["permissions"]:
                    for key, value in changed_keys["permissions"].items():
                        if key in file_dict:
                            changed_dict[key] = value
                            has_changed_keys = True
                        elif key in new_dict:
                            new_dict[key] = value
                            has_new_changed_keys = True

                elif relative_dir == "units.json" and changed_keys["units"]:
                    for key, value in changed_keys["units"].items():
                        if key in file_dict:
                            changed_dict[key] = value
                            has_changed_keys = True
                        elif key in new_dict:
                            new_dict[key] = value
                            has_new_changed_keys = True

                if has_changed_keys:
                    custom_json.save(changed_dict, changed_dir, compact=False)
                    has_changes = True

                if has_new_changed_keys:
                    custom_json.save(new_dict, new_dir, compact=False)
                    has_changes = True

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


def get_files(full_dir):
    """Get dictionaries from files."""
    file_dict = custom_json.load(full_dir)
    if file_dict is None:
        file_dict = {}

    changed_dir = strings.modify_filepath(full_dir, "_CHANGED_")
    changed_dict = custom_json.load(changed_dir)
    if changed_dict is None:
        changed_dict = {}

    new_dir = strings.modify_filepath(full_dir, "_NEW_")
    new_dict = custom_json.load(new_dir)
    if new_dict is None:
        new_dict = {}

    return file_dict, changed_dict, changed_dir, new_dict, new_dir
