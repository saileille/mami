"""Contains CommandRules and RuleSet classes."""
import discord


class CommandRules():
    """Used for checking if the user can use the command."""

    def __init__(self, inclusionary=None, exclusionary=None, sub_commands=None):
        """Object initialisation."""
        self.inclusionary = inclusionary
        self.exclusionary = exclusionary
        self.sub_commands = sub_commands

        if self.inclusionary is None:
            self.inclusionary = CommandRuleSet(True)

        if self.exclusionary is None:
            self.exclusionary = CommandRuleSet(False)

        if self.sub_commands is None:
            self.sub_commands = {}

    @property
    def json_dict(self):
        """Make a dictionary of the object fit for JSON encoding."""
        json_dict = {}

        json_dict["inclusionary"] = self.inclusionary.json_dict
        json_dict["exclusionary"] = self.exclusionary.json_dict

        json_dict["sub_commands"] = {}

        for key in self.sub_commands:
            json_dict["sub_commands"][key] = self.sub_commands[key].json_dict

        return json_dict

    def __str__(self):
        """Get a string representation of the object."""
        string = ("Inclusionary:\n{self.inclusionary}\n\n"
                  "Exclusionary:\n{self.exclusionary}\n\n"
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

        cmd_rules = await self.get_object_from_id_path(command_id_list)
        allow_use = await cmd_rules.inclusionary.check_inclusionary(message)

        if allow_use is None:
            allow_use = await cmd_rules.exclusionary.check_exclusionary(message)

        return allow_use

    async def get_object_from_id_path(self, id_path):
        """
        Get the CommandRules object based on an ID path.

        The function presumes that the ID path is valid.
        """
        cmd_rules = self
        for cmd_id in id_path:
            cmd_rules = cmd_rules.sub_commands[cmd_id]

        return cmd_rules

    async def remove_rule(self, rule):
        """Remove a rule from command rules."""
        branch = None
        if not self.inclusionary.is_empty:
            branch = self.inclusionary
        elif not self.exclusionary.is_empty:
            branch = self.exclusionary
        else:
            return

        if isinstance(rule, discord.Member):
            branch.users.remove(rule.id)
        elif isinstance(rule, discord.Role):
            branch.roles.remove(rule.id)
        elif isinstance(rule, str):
            branch.permissions.remove(rule)

    @staticmethod
    def object_from_json_dict(json_dict):
        """
        Return a CommandRules object from a JSON dictionary.

        The 'JSON' dictionary might not be all, or even any JSON, though. Stay alert!
        """
        obj = CommandRules()

        if isinstance(json_dict, dict):
            for key in json_dict["sub_commands"]:
                obj.sub_commands[key] = CommandRules.object_from_json_dict(
                    json_dict["sub_commands"][key])

            if isinstance(json_dict["inclusionary"], dict):
                obj.inclusionary = CommandRuleSet.object_from_json_dict(json_dict["inclusionary"])
            elif isinstance(json_dict["inclusionary"], CommandRuleSet):
                obj.inclusionary = json_dict["inclusionary"]

            if isinstance(json_dict["exclusionary"], dict):
                obj.exclusionary = CommandRuleSet.object_from_json_dict(json_dict["exclusionary"])
            elif isinstance(json_dict["exclusionary"], CommandRuleSet):
                obj.exclusionary = json_dict["exclusionary"]

        elif isinstance(json_dict, CommandRules):
            for key in json_dict.sub_commands:
                obj.sub_commands[key] = CommandRules.object_from_json_dict(
                    json_dict.sub_commands[key])

            obj.inclusionary = json_dict.inclusionary
            obj.exclusionary = json_dict.exclusionary

        return obj


class CommandRuleSet():
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

        if self.permissions is None and is_inclusionary:
            self.permissions = []
        elif not is_inclusionary:
            self.permissions = None

    @property
    def type(self):
        """
        Determine the object type.

        A simple check to determine if the CommandRuleSet is inclusionary or exclusionary.
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
        return (not self.users and
                not self.roles and
                not self.permissions)

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

    async def add_rule(self, rule):
        """Add user, role or permission to the object."""
        if isinstance(rule, discord.Member):
            if rule.id not in self.users:
                self.users.append(rule.id)
        elif isinstance(rule, discord.Role):
            if rule.id not in self.roles:
                self.roles.append(rule.id)
        elif isinstance(rule, str):
            if rule not in self.permissions:
                self.permissions.append(rule)

    @staticmethod
    def object_from_json_dict(json_dict):
        """
        Return a CommandRuleSet object from a JSON dictionary.

        The 'dictionary' might not be all, or even any JSON, though. Stay alert!
        """
        obj = CommandRuleSet(False)

        if isinstance(json_dict, dict):
            obj.users = json_dict["users"]
            obj.roles = json_dict["roles"]

            if "permissions" in json_dict:
                obj.permissions = json_dict["permissions"]

        elif isinstance(json_dict, CommandRuleSet):
            obj.users = json_dict.users
            obj.roles = json_dict.roles
            obj.permissions = json_dict.permissions

        return obj
