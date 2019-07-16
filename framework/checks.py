"""Contains Checks and CheckSet classes."""


class Checks():
    """Used for checking if the user can use the command."""

    def __init__(self,
                 allow=None,
                 deny=None,
                 sub_commands=None):
        """Object initialisation."""
        self.allow = allow
        self.deny = deny
        self.sub_commands = sub_commands

        if self.allow is None:
            self.allow = CheckSet(True)

        if self.deny is None:
            self.deny = CheckSet(False)

        if self.sub_commands is None:
            self.sub_commands = {}

    @property
    def json_dict(self):
        """Make a dictionary of the object fit for JSON encoding."""
        json_dict = {}

        json_dict["allow"] = self.allow.json_dict
        json_dict["deny"] = self.deny.json_dict

        json_dict["sub_commands"] = {}

        for key in self.sub_commands:
            json_dict["sub_commands"][key] = self.sub_commands[key].json_dict

        return json_dict

    def __str__(self):
        """Get a string representation of the object."""
        string = "Allow:\n{self.allow}\n\n"
        string += "Deny:\n{self.deny}\n\n"
        string += "Sub-Commands:"

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
        allow = await cmd_rules.allow.check_allow(message)

        if allow is None:
            allow = await cmd_rules.deny.check_deny(message)

        return allow

    async def get_object_from_id_path(self, id_path):
        """
        Get the Checks object based on an ID path.

        The function presumes that the ID path is valid.
        """
        cmd_rules = self
        for cmd_id in id_path:
            cmd_rules = cmd_rules.sub_commands[cmd_id]

        return cmd_rules

    @staticmethod
    def object_from_json_dict(json_dict):
        """
        Return a Checks object from a JSON dictionary.

        The 'dictionary' might not be all, or even any JSON, though. Stay alert!
        """
        obj = Checks()

        if isinstance(json_dict, dict):
            for key in json_dict["sub_commands"]:
                obj.sub_commands[key] = Checks.object_from_json_dict(
                    json_dict["sub_commands"][key])

            if isinstance(json_dict["allow"], dict):
                obj.allow = CheckSet.object_from_json_dict(json_dict["allow"])
            elif isinstance(json_dict["allow"], CheckSet):
                obj.allow = json_dict["allow"]

            if isinstance(json_dict["deny"], dict):
                obj.deny = CheckSet.object_from_json_dict(json_dict["deny"])
            elif isinstance(json_dict["deny"], CheckSet):
                obj.deny = json_dict["deny"]

        elif isinstance(json_dict, Checks):
            for key in json_dict.sub_commands:
                obj.sub_commands[key] = Checks.object_from_json_dict(
                    json_dict.sub_commands[key])

            obj.allow = json_dict.allow
            obj.deny = json_dict.deny

        return obj


class CheckSet():
    """Contains set of user, role and permission checks."""

    def __init__(self,
                 is_allow,
                 users=None,
                 roles=None,
                 permissions=None):
        """Object initialisation."""
        self.users = users
        self.roles = roles
        self.permissions = permissions

        if self.users is None:
            self.users = []

        if self.roles is None:
            self.roles = []

        if self.permissions is None and is_allow:
            self.permissions = []
        elif not is_allow:
            self.permissions = None

    @property
    def type(self):
        """
        Determine the object type.

        A simple check to determine if the checkset is allow or deny type.
        """
        if self.permissions is None:
            return "deny"

        return "allow"

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

        if self.type == "allow":
            json_dict["permissions"] = self.permissions

        return json_dict

    def __str__(self):
        """Get a string representation of the object."""
        string = "Users: {self.users}\n"
        string += "Roles: {self.roles}\n"
        string += "Permissions: {self.permissions}"

        return string.format(self=self)

    async def check_allow(self, message):
        """Check the object as allowed type."""
        allow = None

        if self.users:
            allow = message.author.id in self.users

        elif self.roles:
            for user_role in message.author.roles:
                if user_role.id in self.roles:
                    allow = True
                    break
            else:
                allow = False

        elif self.permissions:
            user_permissions = message.channel.permissions_for(message.author)
            for permission_code in self.permissions:
                has_permission = getattr(user_permissions, permission_code)
                if not has_permission:
                    allow = False
                    break
            else:
                allow = True

        # If allow remains None, no explicit allow rules exist, and the check
        # will be handled based on whether the rules are for a channel or a guild.
        return allow

    async def check_deny(self, message):
        """Check the object as deny type."""
        allow = None

        if self.users:
            allow = message.author.id not in self.users

        elif self.roles:
            for user_role in message.author.roles:
                if user_role.id in self.roles:
                    allow = False
                    break
            else:
                allow = True

        # If allow remains None, no explicit allow rules exist, and the check
        # will be handled based on whether the rules are for a channel or a guild.
        return allow

    async def add_rule(self, rule, rule_type):
        """Add user, role or permission to the object."""
        if rule_type == "member":
            if rule.id not in self.users:
                self.users.append(rule.id)
        elif rule_type == "role":
            if rule.id not in self.roles:
                self.roles.append(rule.id)
        elif rule_type == "permission":
            if rule not in self.permissions:
                self.permissions.append(rule)

    @staticmethod
    def object_from_json_dict(json_dict):
        """
        Return a CheckSet object from a JSON dictionary.

        The 'dictionary' might not be all, or even any JSON, though. Stay alert!
        """
        obj = CheckSet(False)

        if isinstance(json_dict, dict):
            obj.users = json_dict["users"]
            obj.roles = json_dict["roles"]

            if "permissions" in json_dict:
                obj.permissions = json_dict["permissions"]

        elif isinstance(json_dict, CheckSet):
            obj.users = json_dict.users
            obj.roles = json_dict.roles
            obj.permissions = json_dict.permissions

        return obj
