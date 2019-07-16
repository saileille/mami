"""Custom exceptions."""


class InvalidCommandException(Exception):
    """Called when the inputted command is invalid."""


class CommandCheckException(Exception):
    """Called when the user is not allowed to use the command due to command rules."""


class PreCheckException(Exception):
    """
    Pre-check exception.

    Called when the user is not allowed to use the command due to circumstancial reasons.
    """


class NoExecutableSubCommands(Exception):
    """Called when there is no executable command that the user can use."""
