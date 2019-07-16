"""Command input."""


class CommandInput():
    """
    Contains commands and arguments in a neat package.

    Has methods to parse raw text into commands and arguments.
    """

    def __init__(self,
                 raw_text):
        """Initialise object."""
        self.raw_text = raw_text.strip()
        self.command_string = ""
        self.arguments = []

        self._commands = None

    def __str__(self):
        """To string method."""
        string = "raw text: {self.raw_text}\n"
        string += "command string: {self.command_string}\n"
        string += "arguments: {self.arguments}\n"
        string += "commands: {self.commands}\n"

        return string.format(self=self)

    @property
    def commands(self):
        """Return a list of commands, separated by a dot."""
        if self._commands is None:
            if self.command_string == "":
                self._commands = []
            else:
                self._commands = self.command_string.split(".")

        return self._commands

    async def parse_raw_text(self):
        """Parse and process command input into commands and arguments."""
        self.command_string = ""
        self.arguments = []

        i = 0
        in_quote = False
        while i < len(self.raw_text):
            i, in_quote = await self.process_letter(i, in_quote)

        if self.raw_text != "":
            self.raw_text = self.raw_text.strip()

            if self.command_string == "":
                self.command_string = self.raw_text
            else:
                self.arguments.append(self.raw_text)

    async def get_prev_letter(self, index):
        """
        Find previous letter of the raw text string.

        Called by parse_raw_text function.
        """
        prev_letter = None
        if index > 0:
            prev_letter = self.raw_text[index - 1]

        return prev_letter

    async def process_letter(self, i, in_quote):
        """
        Identify and process a single letter in raw text string.

        Called by parse_raw_text function.
        """
        letter = self.raw_text[i]
        prev_letter = await self.get_prev_letter(i)

        if letter == " ":
            i = await self.process_space_letter(i, in_quote)
        elif letter == '"' and self.command_string != "" and prev_letter != "\\":
            i, in_quote = await self.process_quotation_mark(i, in_quote)

        i += 1

        return i, in_quote

    async def process_space_letter(self, i, in_quote):
        """
        Identify the context of space character, and react accordingly.

        Called by process_letter function.
        """
        if self.command_string == "":
            self.command_string = self.raw_text[:i]
            self.raw_text = self.raw_text[i:].strip()
            i = -1
        elif not in_quote:
            self.arguments.append(self.raw_text[:i])
            self.raw_text = self.raw_text[i:].strip()
            i = -1

        return i

    async def process_quotation_mark(self, i, in_quote):
        """
        Identify the context of quotation mark, and react accordingly.

        Called by process_letter function.
        """
        if not in_quote:
            # Quote can only start in the first letter.
            self.raw_text = self.raw_text[i + 1:]
        else:
            if i > 0:
                self.arguments.append(self.raw_text[:i])
            else:
                self.arguments.append("")

            self.raw_text = self.raw_text[i + 1:].strip()

        in_quote = not in_quote
        i = -1

        return i, in_quote
