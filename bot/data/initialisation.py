"""Initialise bot data."""
import os
import re

from bot.argument_conversion import command_names
from bot.argument_conversion import currency_codes
from bot.argument_conversion import languages
from bot.argument_conversion import numbers
from bot.argument_conversion import shortcut_names
from bot.argument_conversion import users_and_roles
from bot.commands import currency
from bot.commands import dice
from bot.commands import guild_call
from bot.commands import info
from bot.commands import runes
from bot.commands import settings
from bot.commands import shortcuts
from bot.database import database_functions
from bot.misc import pre_checks
from bot.data import definitions
from framework import custom_json
from framework.argument import Argument
from framework.command import Command
from framework.language import Language


def initialise_commands():
    """Initialise all commands."""
    definitions.COMMANDS = Command(
        sub_commands={
            "currency": Command(
                obj_id="currency",
                sub_commands={
                    "convert": Command(
                        obj_id="convert",
                        action=currency.convert,
                        arguments=[
                            Argument(
                                obj_id="amount",
                                modification=numbers.to_float
                            ),
                            Argument(
                                obj_id="base",
                                modification=currency_codes.valid_currency
                            ),
                            Argument(
                                obj_id="target",
                                modification=currency_codes.valid_currency
                            )
                        ]
                    ),
                    "search": Command(
                        obj_id="search",
                        action=currency.search,
                        arguments=[
                            Argument(
                                obj_id="search_term"
                            )
                        ]
                    ),
                    "display": Command(
                        obj_id="display",
                        action=currency.view_all
                    )
                }
            ),
            "dice": Command(
                obj_id="dice",
                action=dice.throw,
                arguments=[
                    Argument(
                        obj_id="no_of_dice",
                        modification=numbers.valid_no_of_dice
                    ),
                    Argument(
                        obj_id="first_value",
                        modification=numbers.integer
                    ),
                    Argument(
                        obj_id="second_value",
                        modification=numbers.integer
                    )
                ]
            ),
            "guild_call": Command(
                obj_id="guild_call",
                sub_commands={
                    "connect": Command(
                        obj_id="connect",
                        pre_check=pre_checks.is_not_connecting_guild_call,
                        action=guild_call.connect_guild_call
                    ),
                    "disconnect": Command(
                        obj_id="disconnect",
                        pre_check=pre_checks.is_connecting_or_connected_guild_call,
                        action=guild_call.disconnect_guild_call
                    )
                }
            ),
            "info": Command(
                obj_id="info",
                sub_commands={
                    "member": Command(
                        obj_id="member",
                        pre_check=pre_checks.in_guild,
                        action=info.guild_member_info,
                        arguments=[
                            Argument(
                                obj_id="member",
                                modification=users_and_roles.valid_member
                            )
                        ]
                    )
                }
            ),
            "runes": Command(
                obj_id="runes",
                sub_commands={
                    "archaic": Command(
                        obj_id="archaic",
                        action=runes.translate_archaic,
                        arguments=[
                            Argument(
                                obj_id="text"
                            )
                        ]
                    ),
                    "modern": Command(
                        obj_id="modern",
                        action=runes.translate_modern,
                        arguments=[
                            Argument(
                                obj_id="text"
                            )
                        ]
                    ),
                    "musical": Command(
                        obj_id="musical",
                        action=runes.translate_musical,
                        arguments=[
                            Argument(
                                obj_id="text"
                            )
                        ]
                    )
                }
            ),
            "settings": Command(
                obj_id="settings",
                sub_commands={
                    "category": Command(
                        obj_id="category",
                        pre_check=pre_checks.in_category,
                        sub_commands={
                            "command_rules": Command(
                                obj_id="command_rules",
                                default_permissions=[
                                    "administrator"
                                ],
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        sub_commands={
                                            "inclusionary": Command(
                                                obj_id="inclusionary",
                                                action=settings.add_inclusionary_category_command_rule,
                                                arguments=[
                                                    Argument(
                                                        obj_id="commands",
                                                        modification=command_names.commands_to_category_inclusionary_command_rules
                                                    ),
                                                    Argument(
                                                        obj_id="rule",
                                                        modification=users_and_roles.member_role_permission
                                                    )
                                                ],
                                                unlimited_arguments=True
                                            ),
                                            "exclusionary": Command(
                                                obj_id="exclusionary",
                                                action=settings.add_exclusionary_category_command_rule,
                                                arguments=[
                                                    Argument(
                                                        obj_id="commands",
                                                        modification=command_names.commands_to_category_exclusionary_command_rules
                                                    ),
                                                    Argument(
                                                        obj_id="rule",
                                                        modification=users_and_roles.member_role
                                                    )
                                                ],
                                                unlimited_arguments=True
                                            )
                                        }
                                    ),
                                    "remove": Command(
                                        obj_id="remove",
                                        action=settings.remove_category_command_rule,
                                        arguments=[
                                            Argument(
                                                obj_id="commands",
                                                modification=command_names.commands_to_category_command_rules
                                            ),
                                            Argument(
                                                obj_id="rule",
                                                modification=users_and_roles.member_role_permission
                                            )
                                        ],
                                        unlimited_arguments=True
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        action=settings.display_category_command_rules,
                                        arguments=[
                                            Argument(
                                                obj_id="command",
                                                modification=command_names.command_to_non_empty_category_command_rules
                                            )
                                        ]
                                    )
                                }
                            ),
                            "language": Command(
                                obj_id="language",
                                sub_commands={
                                    "reset": Command(
                                        obj_id="reset",
                                        pre_check=pre_checks.category_has_language,
                                        action=settings.reset_category_language,
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    ),
                                    "set": Command(
                                        obj_id="set",
                                        action=settings.set_category_language,
                                        arguments=[
                                            Argument(
                                                obj_id="language",
                                                modification=languages.language_id
                                            )
                                        ],
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    )
                                }
                            ),
                            "shortcut": Command(
                                obj_id="shortcut",
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        action=shortcuts.add_category_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_not_category_shortcut_name,
                                            ),
                                            Argument(
                                                obj_id="content"
                                            )
                                        ]
                                    ),
                                    "delete": Command(
                                        obj_id="delete",
                                        action=shortcuts.delete_category_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_category_shortcut_name
                                            )
                                        ],
                                        default_permissions=["manage_messages"]
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        pre_check=pre_checks.category_has_shortcuts,
                                        action=shortcuts.display_category_shortcuts
                                    )
                                }
                            )
                        }
                    ),
                    "channel": Command(
                        obj_id="channel",
                        pre_check=pre_checks.in_guild,
                        sub_commands={
                            "command_rules": Command(
                                obj_id="command_rules",
                                default_permissions=[
                                    "administrator"
                                ],
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        sub_commands={
                                            "inclusionary": Command(
                                                obj_id="inclusionary",
                                                action=settings.add_inclusionary_channel_command_rule,
                                                arguments=[
                                                    Argument(
                                                        obj_id="commands",
                                                        modification=command_names.commands_to_channel_inclusionary_command_rules
                                                    ),
                                                    Argument(
                                                        obj_id="rule",
                                                        modification=users_and_roles.member_role_permission
                                                    )
                                                ],
                                                unlimited_arguments=True
                                            ),
                                            "exclusionary": Command(
                                                obj_id="exclusionary",
                                                action=settings.add_exclusionary_channel_command_rule,
                                                arguments=[
                                                    Argument(
                                                        obj_id="commands",
                                                        modification=command_names.commands_to_channel_exclusionary_command_rules
                                                    ),
                                                    Argument(
                                                        obj_id="rule",
                                                        modification=users_and_roles.member_role
                                                    )
                                                ],
                                                unlimited_arguments=True
                                            )
                                        }
                                    ),
                                    "remove": Command(
                                        obj_id="remove",
                                        action=settings.remove_channel_command_rule,
                                        arguments=[
                                            Argument(
                                                obj_id="commands",
                                                modification=command_names.commands_to_channel_command_rules
                                            ),
                                            Argument(
                                                obj_id="rule",
                                                modification=users_and_roles.member_role_permission
                                            )
                                        ],
                                        unlimited_arguments=True
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        action=settings.display_channel_command_rules,
                                        arguments=[
                                            Argument(
                                                obj_id="command",
                                                modification=command_names.command_to_non_empty_channel_command_rules
                                            )
                                        ]
                                    )
                                }
                            ),
                            "language": Command(
                                obj_id="language",
                                sub_commands={
                                    "reset": Command(
                                        obj_id="reset",
                                        pre_check=pre_checks.channel_has_language,
                                        action=settings.reset_channel_language,
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    ),
                                    "set": Command(
                                        obj_id="set",
                                        action=settings.set_channel_language,
                                        arguments=[
                                            Argument(
                                                obj_id="language",
                                                modification=languages.language_id
                                            )
                                        ],
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    )
                                }
                            ),
                            "shortcut": Command(
                                obj_id="shortcut",
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        action=shortcuts.add_channel_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_not_channel_shortcut_name,
                                            ),
                                            Argument(
                                                obj_id="content"
                                            )
                                        ]
                                    ),
                                    "delete": Command(
                                        obj_id="delete",
                                        action=shortcuts.delete_channel_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_channel_shortcut_name
                                            )
                                        ],
                                        default_permissions=["manage_messages"]
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        pre_check=pre_checks.channel_has_shortcuts,
                                        action=shortcuts.display_channel_shortcuts
                                    )
                                }
                            )
                        }
                    ),
                    "guild": Command(
                        obj_id="guild",
                        pre_check=pre_checks.in_guild,
                        sub_commands={
                            "command_rules": Command(
                                obj_id="command_rules",
                                default_permissions=[
                                    "administrator"
                                ],
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        sub_commands={
                                            "inclusionary": Command(
                                                obj_id="inclusionary",
                                                action=settings.add_inclusionary_guild_command_rule,
                                                arguments=[
                                                    Argument(
                                                        obj_id="commands",
                                                        modification=command_names.commands_to_guild_inclusionary_command_rules
                                                    ),
                                                    Argument(
                                                        obj_id="rule",
                                                        modification=users_and_roles.member_role_permission
                                                    )
                                                ],
                                                unlimited_arguments=True
                                            ),
                                            "exclusionary": Command(
                                                obj_id="exclusionary",
                                                action=settings.add_exclusionary_guild_command_rule,
                                                arguments=[
                                                    Argument(
                                                        obj_id="commands",
                                                        modification=command_names.commands_to_guild_exclusionary_command_rules
                                                    ),
                                                    Argument(
                                                        obj_id="rule",
                                                        modification=users_and_roles.member_role
                                                    )
                                                ],
                                                unlimited_arguments=True
                                            )
                                        }
                                    ),
                                    "remove": Command(
                                        obj_id="remove",
                                        action=settings.remove_guild_command_rule,
                                        arguments=[
                                            Argument(
                                                obj_id="commands",
                                                modification=command_names.commands_to_guild_command_rules
                                            ),
                                            Argument(
                                                obj_id="rule",
                                                modification=users_and_roles.member_role_permission
                                            )
                                        ],
                                        unlimited_arguments=True
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        action=settings.display_guild_command_rules,
                                        arguments=[
                                            Argument(
                                                obj_id="command",
                                                modification=command_names.command_to_non_empty_guild_command_rules
                                            )
                                        ]
                                    )
                                }
                            ),
                            "language": Command(
                                obj_id="language",
                                sub_commands={
                                    "reset": Command(
                                        obj_id="reset",
                                        pre_check=pre_checks.guild_has_language,
                                        action=settings.reset_guild_language,
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    ),
                                    "set": Command(
                                        obj_id="set",
                                        action=settings.set_guild_language,
                                        arguments=[
                                            Argument(
                                                obj_id="language",
                                                modification=languages.language_id
                                            )
                                        ],
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    )
                                }
                            ),
                            "shortcut": Command(
                                obj_id="shortcut",
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        action=shortcuts.add_guild_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_not_guild_shortcut_name,
                                            ),
                                            Argument(
                                                obj_id="content"
                                            )
                                        ]
                                    ),
                                    "delete": Command(
                                        obj_id="delete",
                                        action=shortcuts.delete_guild_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_guild_shortcut_name
                                            )
                                        ],
                                        default_permissions=["manage_messages"]
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        pre_check=pre_checks.guild_has_shortcuts,
                                        action=shortcuts.display_guild_shortcuts
                                    )
                                }
                            )
                        }
                    ),
                    "user": Command(
                        obj_id="user",
                        sub_commands={
                            "language": Command(
                                obj_id="language",
                                sub_commands={
                                    "reset": Command(
                                        obj_id="reset",
                                        pre_check=pre_checks.user_has_language,
                                        action=settings.reset_user_language,
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    ),
                                    "set": Command(
                                        obj_id="set",
                                        action=settings.set_user_language,
                                        arguments=[
                                            Argument(
                                                obj_id="language",
                                                modification=languages.language_id
                                            )
                                        ],
                                        default_permissions=[
                                            "administrator"
                                        ]
                                    )
                                }
                            ),
                            "shortcut": Command(
                                obj_id="shortcut",
                                sub_commands={
                                    "add": Command(
                                        obj_id="add",
                                        action=shortcuts.add_user_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_not_user_shortcut_name,
                                            ),
                                            Argument(
                                                obj_id="content"
                                            )
                                        ]
                                    ),
                                    "delete": Command(
                                        obj_id="delete",
                                        action=shortcuts.delete_user_shortcut,
                                        arguments=[
                                            Argument(
                                                obj_id="name",
                                                modification=shortcut_names.is_user_shortcut_name
                                            )
                                        ]
                                    ),
                                    "display": Command(
                                        obj_id="display",
                                        pre_check=pre_checks.user_has_shortcuts,
                                        action=shortcuts.display_user_shortcuts
                                    )
                                }
                            )
                        }
                    )
                }
            ),
            "shortcut": Command(
                obj_id="shortcut",
                action=shortcuts.use_shortcut,
                arguments=[
                    Argument(
                        obj_id="name",
                        modification=shortcut_names.any_shortcut
                    )
                ]
            )
        }
    )

    guild_default_command_rules, empty_command_rules = definitions.COMMANDS.initialise_commands()

    definitions.GUILD_DEFAULT_COMMAND_RULES = custom_json.save(guild_default_command_rules)
    definitions.EMPTY_COMMAND_RULES = custom_json.save(empty_command_rules)


def initialise_languages():
    """Create language objects and fill them with keys."""
    is_language_folder = r"^[^\\\.]*"    # Cannot have backslash or dot.
    language_folder_path = os.path.join(definitions.ROOT_DIR, "languages")

    for root, dirs, files in os.walk(language_folder_path):
        for name in files:
            if name.startswith("_NEW_") or name.startswith("_CHANGED_"):
                # Files that are auto-generated will not be added.
                continue

            full_dir = os.path.join(root, name)
            relative_dir = full_dir.replace(language_folder_path + "\\", "")

            match = re.match(is_language_folder, relative_dir)
            language_id = match.group(0)

            language = None
            if language_id != "cache":
                language = definitions.LANGUAGES[language_id]
            else:
                language = definitions.CACHE_LANGUAGE

            if relative_dir == "{id}\\commands.json".format(id=language_id):
                # Take the commands.
                definitions.COMMANDS.add_command_localisation(full_dir, language_id)

            elif relative_dir == "{id}\\languages.json".format(id=language_id):
                # Take the languages.
                language.add_languages(full_dir)

            elif relative_dir == "{id}\\meta.json".format(id=language_id):
                # Take the metadata.
                language.add_meta(full_dir)

            elif relative_dir == "{id}\\permissions.json".format(id=language_id):
                # Take the permissions.
                language.add_permission_names(full_dir)

            elif relative_dir == "{id}\\units.json".format(id=language_id):
                language.add_units(full_dir)

            else:
                # Take the keys
                language.add_keys_from_path(full_dir)

        for name in dirs:
            full_dir = os.path.join(root, name)
            relative_dir = full_dir.replace(language_folder_path + "\\", "")

            match = re.fullmatch(is_language_folder, relative_dir)
            if match is not None:
                if name != "cache":
                    definitions.LANGUAGES[name] = Language(name)
                else:
                    definitions.CACHE_LANGUAGE = Language(name)


def update_config_data():
    """
    Update the config data.

    Updates the previously saved config data to be compatible with new versions of Mami.
    Called on startup.
    """
    channels = database_functions.select_all_channels()
    for channel_id in channels:
        channel = channels[channel_id]
        channel_command_rules = channel.command_rules.sub_commands
        channel_default_command_rules = custom_json.load(
            definitions.EMPTY_COMMAND_RULES).sub_commands

        synchronise_command_rule_objects(
            channel_default_command_rules, channel_command_rules)

        if (channel.language_id is not None and
            channel.language_id not in definitions.LANGUAGES):
            channel.language_id = None

        database_functions.synchronise_channel_update(channel_id, channel)

    categories = database_functions.select_all_categories()
    for category_id in categories:
        category = categories[category_id]
        category_command_rules = category.command_rules.sub_commands
        category_default_command_rules = custom_json.load(
            definitions.EMPTY_COMMAND_RULES,).sub_commands

        synchronise_command_rule_objects(
            category_default_command_rules, category_command_rules)

        if (category.language_id is not None and
            category.language_id not in definitions.LANGUAGES):
            category.language_id = None

        database_functions.synchronise_category_update(category_id, category)

    guilds = database_functions.select_all_guilds()
    for guild_id in guilds:
        guild = guilds[guild_id]
        guild_command_rules = guild.command_rules.sub_commands
        guild_default_command_rules = custom_json.load(
            definitions.GUILD_DEFAULT_COMMAND_RULES).sub_commands

        synchronise_command_rule_objects(guild_default_command_rules, guild_command_rules)
        if (guild.language_id is not None and
            guild.language_id not in definitions.LANGUAGES):
            guild.language_id = None

        database_functions.synchronise_guild_update(guild_id, guild)

    users = database_functions.select_all_users()
    for user_id in users:
        user = users[user_id]
        if (user.language_id is not None and
            user.language_id not in definitions.LANGUAGES):
            user.language_id = None

        database_functions.synchronise_user_update(user_id, user)


def synchronise_command_rule_objects(default, control):
    """
    Make a command rule dictionary have the same entries as the default one.

    Helper function. First deletes all command rules from commands which no longer exist.
    Then adds any possible new commands to the control dictionary and moves on to the
    sub-commands.
    """
    delete_obsolete_command_items(default, control)

    for cmd_id in default:
        if cmd_id not in control:
            control[cmd_id] = default[cmd_id]

        synchronise_command_rule_objects(
            default[cmd_id].sub_commands, control[cmd_id].sub_commands)


def delete_obsolete_command_items(default, control):
    """Delete data which no longer exists."""
    delete_keys = []
    for cmd_id in control:
        if cmd_id not in default:
            delete_keys.append(cmd_id)

    for key in delete_keys:
        del control[key]
