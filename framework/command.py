"""Import stuff."""
import json

from bot.misc import embed_messages
from bot.data import default_values
from bot.data import definitions
from framework import exceptions
from framework.command_data import CommandData


class Command():
    """
    Command class.

    obj_id - string
    pre_check - function
    action - function
    nsfw_action - function
    arguments - list of Argument
    unlimited_arguments - boolean
    default_permissions - list of string
    sub_commands - dictionary of Command
    """

    def __init__(
            self, obj_id=None, related_commands=None, pre_check=None, action=None,
            nsfw_action=None, arguments=None, unlimited_arguments=False,
            default_permissions=None, sub_commands=None):
        """Object initialisation."""
        self.obj_id = obj_id
        self._related_commands = related_commands
        self.pre_check = pre_check
        self.action = action
        self.nsfw_action = nsfw_action
        self.arguments = arguments
        self.unlimited_arguments = unlimited_arguments
        self.default_permissions = default_permissions
        self.sub_commands = sub_commands

        self.localisation = {}
        self.parent_commands = []

        if self._related_commands is None:
            self._related_commands = []

        if self.arguments is None:
            self.arguments = []

        if self.sub_commands is None:
            self.sub_commands = {}

        if self.default_permissions is None:
            self.default_permissions = []

    @property
    def id_path(self):
        """Get all IDs of the parent commands and this command."""
        id_path = self.parent_commands[:]
        if self.obj_id is not None:
            id_path += [self.obj_id]

        return id_path

    @property
    def related_commands(self):
        """Get related commands."""
        if self._related_commands and isinstance(self._related_commands[0], list):
            root_cmd = definitions.COMMANDS
            for i, id_list in enumerate(self._related_commands):
                self._related_commands[i] = root_cmd.get_sub_command_from_path(id_list)

        return self._related_commands

    def add_localisation(self, language_id, localisation_pack):
        """
        Add appropriate localisation to the command.

        1) Add command localisation.
        2) If arguments exist, call argument localisation method.
        """
        self.localisation[language_id] = {}
        self.localisation[language_id]["names"] = localisation_pack["names"]
        self.localisation[language_id]["description"] = localisation_pack["description"]
        self.localisation[language_id]["help_text"] = localisation_pack["help_text"]

        if "arguments" in localisation_pack:
            self.add_argument_localisation(localisation_pack["arguments"], language_id)

    def add_argument_localisation(self, localisation_pack, language_id):
        """
        Call argument localisation.

        1) Loop through arguments.
        2) Call argument class' localisation method on them.
        """
        for argument in self.arguments:
            argument.add_localisation(language_id, localisation_pack[argument.obj_id])

    def add_command_localisation(self, full_dir, language_id):
        """Add command localisation."""
        command_localisation = None
        with open(full_dir, "r", encoding="utf-8") as file:
            try:
                command_localisation = json.load(file)
            except json.decoder.JSONDecodeError:
                command_localisation = {}

        self.add_sub_command_localisation(command_localisation, language_id)

    def add_sub_command_localisation(self, command_localisation, language_id):
        """
        Go through sub-commands and add localisation to them.

        1) Iterate sub-commands.
        2) Call localisation method on the sub-command.
        3) Recurse this method using this sub-command's sub-commands.
        4) Once the bottom of sub-commands is reached, returns to the original loop and
        goes to the next item.
        """
        for sub_command in self.sub_commands.values():
            localisation_pack = command_localisation[sub_command.obj_id]
            sub_command.add_localisation(language_id, localisation_pack)

            if "sub_commands" in localisation_pack:
                sub_command.add_sub_command_localisation(
                    localisation_pack["sub_commands"], language_id)

    def initialise_commands(self, parent_commands=None):
        """
        Initialise command stuffs.

        Add parent command list for the command
        Construct the default CommandData JSON.
        """
        guild_command_data = CommandData()
        default_command_data = CommandData()
        user_command_data = CommandData(has_command_rules=False)
        if parent_commands is None:
            parent_commands = []

        self.initialise_parent_commands(parent_commands)

        for permission in self.default_permissions:
            guild_command_data.command_rules.permissions.append(permission)

        for sub_command in self.sub_commands.values():
            guild_command_data.sub_commands[sub_command.obj_id], default_command_data.sub_commands[sub_command.obj_id], user_command_data.sub_commands[sub_command.obj_id] = sub_command.initialise_commands(parent_commands[:])

        return guild_command_data, default_command_data, user_command_data

    def initialise_parent_commands(self, parent_commands):
        """Record the parent commands of the command."""
        self.parent_commands = parent_commands[:]
        if self.obj_id is not None:
            # Condition prevents the root ID from being included.
            parent_commands.append(self.obj_id)

    def create_language_data(self, language_id):
        """Create the language data template for a given command."""
        default_localisation = None
        if default_values.LANGUAGE_ID in self.localisation:
            default_localisation = self.localisation[default_values.LANGUAGE_ID]
        elif language_id == default_values.LANGUAGE_ID:
            default_localisation = {"names": [], "description": "", "help_text": ""}
        else:
            return None

        localisation = {
            "names": default_localisation["names"],
            "description": default_localisation["description"],
            "help_text": default_localisation["help_text"]}

        if self.arguments:
            localisation["arguments"] = {}
            for argument in self.arguments:
                localisation["arguments"][argument.obj_id] = argument.create_language_data(
                    language_id)

        if self.sub_commands:
            localisation["sub_commands"] = {}
            for sub_command in self.sub_commands.values():
                localisation["sub_commands"][sub_command.obj_id] = (
                    sub_command.create_language_data(language_id))

        return localisation

    def get_sub_command_from_path(self, *id_list):
        """
        Get a sub-command with the given ID path.

        The function presumes that the ID path is valid.
        """
        if isinstance(id_list[0], list):
            id_list = id_list[0]

        command = self
        for cmd_id in id_list:
            command = command.sub_commands[cmd_id]

        return command

    async def execute(self, context, command_input):
        """
        Execute the command.

        Return whether command-use was completed fully and successfully.
        """
        if self.action is None:
            await self.no_action(context, command_input)
            return True

        # Argument handling
        valid_arguments = await self.validate_arguments(
            context, command_input.arguments)

        if not valid_arguments:
            return False

        return await self.action(context, command_input.arguments)

    async def get_command_string(self, context, include_prefix=True):
        """Get the command string with the context language."""
        commands = definitions.COMMANDS.sub_commands
        command_names = []

        for cmd_id in self.parent_commands:
            command_names.append(
                commands[cmd_id].localisation[context.language_id]["names"][0])

            commands = commands[cmd_id].sub_commands

        if self.obj_id is not None:
            command_names.append(self.localisation[context.language_id]["names"][0])

        command_string = ".".join(command_names)
        if include_prefix:
            command_string = context.prefix + command_string

        return command_string

    async def get_sub_commands(self, context, filter_unallowed=True):
        """Get a list of sub-commands."""
        sub_commands = []
        for sub_command in self.sub_commands.values():
            if (not filter_unallowed or
                await sub_command.check_if_allowed(context, verbose=False) is None):
                sub_commands.append(sub_command)

        return sub_commands

    async def get_sub_command_names(
            self, context, command_input=None, include_prefix=True,
            filter_unallowed=True):
        """
        Get a list of sub-command names.

        Can be used in embed messages.
        """
        command_string = None
        if command_input is None:
            command_string = await self.get_command_string(context, include_prefix)
        else:
            command_string = command_input.command_string
            if include_prefix:
                command_string = context.prefix + command_string

        if self.obj_id is not None:
            command_string += "."

        commands = []
        for sub_command in self.sub_commands.values():
            command_name = sub_command.localisation[context.language_id]["names"][0]
            if (not filter_unallowed or
                await sub_command.check_if_allowed(context, verbose=False) is None):
                commands.append(command_string + command_name)

        commands.sort()
        return commands

    async def check_if_allowed(self, context, verbose=True):
        """
        Check if the command can be used.

        If the command is allowed to be used, return None.
        If the command is not allowed to be used, return the appropriate exception.
        """
        exception = await self.check_usage(context, verbose)
        if exception is not None or self.action is not None:
            return exception

        for sub_command in self.sub_commands.values():
            exception = await sub_command.check_if_allowed(context, verbose=False)
            if exception is None:
                return exception

        return exceptions.NoExecutableSubCommands

    async def check_usage(self, context, verbose=True):
        """Check if command cannot be used, does not check sub-commands."""
        exception = None

        # Pre-check
        if self.pre_check is not None and not await self.pre_check(context, verbose):
            exception = exceptions.PreCheckException

        # Permission checks.
        elif (context.message.guild is not None and
              not await context.check_command_rules(self.id_path)):
            exception = exceptions.CommandCheckException

        return exception

    async def no_action(self, context, command_input):
        """
        Send a message with sub-commands.

        Used when there is no action function defined.
        """
        commands = await self.get_sub_command_names(context, command_input)
        command_string = context.prefix + command_input.command_string

        await embed_messages.no_action(context, commands, command_string)

    async def invalid_command(self, context, command_input):
        """Handle invalid commands."""
        if self.sub_commands:
            await self.invalid_command_subcommands(context, command_input)
        else:
            await self.invalid_command_no_subcommands(context, command_input)

    async def invalid_command_subcommands(self, context, command_input):
        """
        Send a message with sub-commands.

        Used when there is an invalid command used, and when the command has sub-commands.
        """
        commands = await self.get_sub_command_names(context)
        command_string = context.prefix + command_input.command_string
        last_working_command_string = await self.get_command_string(context)

        await embed_messages.invalid_command_subcommands(
            context, commands, command_string, last_working_command_string)

    async def invalid_command_no_subcommands(self, context, command_input):
        """
        Send a message informing of the last valid command.

        Used when there is an invalid command used, and when the command has no
        sub-commands.
        """
        command_string = context.prefix + command_input.command_string
        last_working_command_string = await self.get_command_string(context)

        await embed_messages.invalid_command_no_subcommands(
            context, command_string, last_working_command_string)

    async def not_authorised(self, context, command_input):
        """
        Send a message informing of the last authorised command.

        Used when the user entered a command they are not authorised to use.
        """
        command_string = context.prefix + command_input.command_string
        last_working_command_string = await self.get_command_string(context)

        await embed_messages.not_authorised(
            context, command_string, last_working_command_string)

    async def no_usable_sub_commands(self, context, command_input):
        """
        Send a message informing of the last usable command.

        Used when the user entered a command which does not have any usable sub-commands.
        """
        command_string = context.prefix + command_input.command_string
        last_working_command_string = await self.get_command_string(context)

        await embed_messages.no_usable_sub_commands(
            context, command_string, last_working_command_string)

    async def validate_given_arguments(self, context, arguments):
        """Validate and convert the arguments that have been given by the user."""
        for i, argument in enumerate(arguments):
            converted_argument = None
            arg_index = None

            if i < len(self.arguments):
                arg_index = i
            elif self.unlimited_arguments:
                arg_index = -1
            else:
                # More arguments than allowed.
                await embed_messages.too_many_arguments(
                    context, len(self.arguments), argument)

                return False

            converted_argument = await self.arguments[arg_index].convert(
                argument, context)

            if converted_argument is None:
                return False

            arguments[i] = converted_argument

        return True

    async def validate_missing_arguments(self, context, arguments):
        """Ask for missing arguments, validate and convert them."""
        argument_amount = len(self.arguments)

        while len(arguments) < argument_amount or self.unlimited_arguments:
            arguments_given = len(arguments)

            i = None
            optional_argument = None
            if arguments_given < argument_amount:
                i = arguments_given
                optional_argument = False
            else:
                i = -1
                optional_argument = True

            converted_argument = None
            while converted_argument is None:
                argument = await self.arguments[i].dialogue(
                    context, optional_argument, arguments_given + 1, argument_amount)

                # If cancel button is pressed.
                if argument is None:
                    # If optional argument.
                    if optional_argument:
                        return True

                    # If not optional argument.
                    await context.message.channel.send(
                        await context.language.get_text("command_aborted"))

                    return False

                converted_argument = await self.arguments[i].convert(argument, context)

            arguments.append(converted_argument)

        return True

    async def validate_arguments(self, context, arguments):
        """
        Validate and convert arguments.

        1) Validate and convert all given arguments.
        2.1) If there are arguments missing, ask for them from the user.
        2.2) Validate and convert.
        """
        valid = await self.validate_given_arguments(context, arguments)
        if not valid:
            return False

        valid = await self.validate_missing_arguments(context, arguments)

        return valid
