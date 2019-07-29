"""Guild-call-related mechanics."""


class GuildCall():
    """Guild call object."""

    def __init__(self, connected_channel=None, connecting=False):
        """Initialise object."""
        self.connected_channel = connected_channel
        self.connecting = connecting
