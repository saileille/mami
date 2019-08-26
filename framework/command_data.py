"""Contains CommandData and CommandRules classes."""
import discord


class CommandData():
    """Command data."""

    def __init__(
            self, command_rules=None, use_times=0, sub_commands=None,
            has_command_rules=True):
        """Object initialisation."""
        self.command_rules = command_rules
        self.use_times = use_times
        self.sub_commands = sub_commands

        if has_command_rules and self.command_rules is None:
            self.command_rules = CommandRules(True)

        if self.sub_commands is None:
            self.sub_commands = {}

    @property
    def json_dict(self):
        """Make a dictionary of the object fit for JSON encoding."""
        json_dict = {}

        if self.command_rules is not None:
            json_dict["command_rules"] = self.command_rules.json_dict

        json_dict["use_times"] = self.use_times

        json_dict["sub_commands"] = {}

        for key in self.sub_commands:
            json_dict["sub_commands"][key] = self.sub_commands[key].json_dict

        return json_dict

    def __str__(self):
        """Get a string representation of the object."""
        string = ("Command Rules:\n{self.command_rules}\n\n"
                  "Use Times: {self.use_times}\n"
                  "Sub-Commands:")

        for key in self.sub_commands:
            sub_command = self.sub_commands[key]
            string += "\n{key}:\n{sub_command}".format(sub_command=sub_command, key=key)

        return string.format(self=self)

    async def check_rules(self, message, command_id_list):
        """Go through the check rules."""
        # If the user is the guild owner, no questions are asked.
        if message.channel.guild.owner.id == message.author.id:
            return True

        data = await self.get_object_from_id_path(command_id_list)
        return await data.command_rules.check_rules(message)

    async def get_object_from_id_path(self, id_path):
        """
        Get the CommandData object based on an ID path.

        The function presumes that the ID path is valid.
        """
        cmd_data = self
        for cmd_id in id_path:
            cmd_data = cmd_data.sub_commands[cmd_id]

        return cmd_data

    async def add_command_use(self, command_id_list):
        """Add one command use to the statistics."""
        data = await self.get_object_from_id_path(command_id_list)
        data.use_times += 1

    @staticmethod
    def object_from_json_dict(json_dict):
        """
        Return a CommandData object from a JSON dictionary.

        The 'JSON' dictionary might not be all, or even any JSON, though. Stay alert!
        """
        obj = CommandData(has_command_rules=False)

        if isinstance(json_dict, dict):
            for key in json_dict["sub_commands"]:
                obj.sub_commands[key] = CommandData.object_from_json_dict(
                    json_dict["sub_commands"][key])

            if "command_rules" in json_dict:
                if isinstance(json_dict["command_rules"], dict):
                    obj.command_rules = CommandRules.object_from_json_dict(
                        json_dict["command_rules"])

                elif isinstance(json_dict["command_rules"], CommandRules):
                    obj.command_rules = json_dict["command_rules"]

            obj.use_times = json_dict["use_times"]

        elif isinstance(json_dict, CommandData):
            for key in json_dict.sub_commands:
                obj.sub_commands[key] = CommandData.object_from_json_dict(
                    json_dict.sub_commands[key])

            obj.command_rules = json_dict.command_rules
            obj.use_times = json_dict.use_times

        return obj


class CommandRules():
    """Contains set of user, role and permission checks."""

    def __init__(self, is_inclusionary, users=None, roles=None, permissions=None):
        """Object initialisation."""
        self.users = users
        self.roles = roles
        self.permissions = permissions

        if self.users is None:
            self.users = []

        if self.roles is None:
            self.roles = []

        if self.permissions is None:
            if is_inclusionary:
                self.permissions = []
            else:
                self.permissions = None

    @property
    def type(self):
        """
        Determine the command rule type.

        A simple check to determine if the CommandRules is inclusionary or exclusionary.
        """
        if self.permissions is None:
            return "exclusionary"

        return "inclusionary"

    @property
    def is_empty(self):
        """
        Check if the object contains any set rules.

        Return True if object is void of data.
        Return False if object has data.
        """
        return not (self.users or self.roles or self.permissions)

    @property
    def json_dict(self):
        """Make a dictionary of the object fit for JSON encoding."""
        json_dict = {"users": self.users,
                     "roles": self.roles}

        if self.type == "inclusionary":
            json_dict["permissions"] = self.permissions

        return json_dict

    def __str__(self):
        """Get a string representation of the object."""
        return ("Users: {self.users}\n"
                "Roles: {self.roles}\n"
                "Permissions: {self.permissions}").format(self=self)

    async def check_rules(self, message):
        """Check the command rules."""
        if self.type == "inclusionary":
            return await self.check_inclusionary(message)

        return await self.check_exclusionary(message)

    async def check_inclusionary(self, message):
        """Check the object as inclusionary."""
        allow_use = None

        if self.users:
            allow_use = message.author.id in self.users

        elif self.roles:
            for user_role in message.author.roles:
                if user_role.id in self.roles:
                    allow_use = True
                    break
            else:
                allow_use = False

        elif self.permissions:
            user_permissions = message.channel.permissions_for(message.author)
            for permission_code in self.permissions:
                has_permission = getattr(user_permissions, permission_code)
                if not has_permission:
                    allow_use = False
                    break
            else:
                allow_use = True

        # If allow_use remains None, no explicit inclusionary rules exist, and the check
        # will be handled based on whether the rules are for channel, category or guild.
        return allow_use

    async def check_exclusionary(self, message):
        """Check the object as exclusionary."""
        allow_use = None

        if self.users:
            allow_use = message.author.id not in self.users

        elif self.roles:
            for user_role in message.author.roles:
                if user_role.id in self.roles:
                    allow_use = False
                    break
            else:
                allow_use = True

        # If allow_use remains None, no explicit exclusionary rules exist, and the check
        # will be handled based on whether the rules are for channel, category or guild.
        return allow_use

    async def add_rule(self, rule, ruletype):
        """Add user, role or permission to the object."""
        if ruletype == "inclusionary" and self.type != "inclusionary":
            self.permissions = []
        elif ruletype == "exclusionary" and self.type != "exclusionary":
            self.permissions = None

        if isinstance(rule, discord.Member):
            if rule.id not in self.users:
                self.users.append(rule.id)
        elif isinstance(rule, discord.Role):
            if rule.id not in self.roles:
                self.roles.append(rule.id)
        elif isinstance(rule, str):
            if rule not in self.permissions:
                self.permissions.append(rule)

    async def remove_rule(self, rule):
        """Remove a rule from command rules."""
        if isinstance(rule, discord.Member):
            self.users.remove(rule.id)
        elif isinstance(rule, discord.Role):
            self.roles.remove(rule.id)
        elif isinstance(rule, str):
            self.permissions.remove(rule)

    @staticmethod
    def object_from_json_dict(json_dict):
        """
        Return a CommandRules object from a JSON dictionary.

        The 'dictionary' might not be all, or even any JSON, though. Stay alert!
        """
        obj = CommandRules(False)

        if isinstance(json_dict, dict):
            obj.users = json_dict["users"]
            obj.roles = json_dict["roles"]

            if "permissions" in json_dict:
                obj.permissions = json_dict["permissions"]

        elif isinstance(json_dict, CommandRules):
            obj.users = json_dict.users
            obj.roles = json_dict.roles
            obj.permissions = json_dict.permissions

        return obj
