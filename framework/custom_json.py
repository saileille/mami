"""Import stuff."""
import json
import os

from framework import command_rules


class JSONEncoder(json.JSONEncoder):
    """Custom JSON Encoder."""

    def default(self, o):   # pylint: disable=E0202
        """Encode JSON."""
        return o.json_dict

        # Let the base class default method raise the TypeError
        # return json.JSONEncoder.default(self, o)


def decode(json_dict):
    """
    Load JSON with customised functionality.

    Used as object_hook parameter in json.loads() function.
    """
    if "users" in json_dict and "roles" in json_dict:
        return command_rules.CommandRuleSet.object_from_json_dict(json_dict)

    if ("inclusionary" in json_dict and
        "exclusionary" in json_dict and
        "sub_commands" in json_dict):
        return command_rules.CommandRules.object_from_json_dict(json_dict)

    return json_dict


def load(directory_or_json):
    """
    Load JSON data with desired options.

    If the parametre is a valid directory, load JSON from there.
    If the parametre is not a valid directory, attempt to parse it as JSON.
    """
    json_string = None
    try:
        with open(directory_or_json, "r", encoding="utf-8") as file:
            json_string = file.read()
    except OSError:
        json_string = directory_or_json

    json_object = None
    try:
        json_object = json.loads(json_string, encoding="utf-8", object_hook=decode)
    except json.JSONDecodeError:
        pass

    return json_object


def save(data, directory=None, compact=True):
    """
    Save or stringify JSON data with desired options.

    If directory is not None, a JSON string gets saved in the location.
    In either case, the stringified JSON data is returned.

    Formatting can be either compact or readable. Readable format means that 2 indent
    spaces are being used.
    """
    indent = None
    separators = (",", ":")
    if not compact:
        indent = 2
        separators = (",", ": ")

    json_string = json.dumps(
        data, cls=JSONEncoder, ensure_ascii=False, indent=indent, separators=separators,
        sort_keys=True)

    if directory is not None:
        folder = "\\".join(directory.split("\\")[:-1])
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(directory, "w+", encoding="utf-8") as file:
            file.write(json_string)

    return json_string
