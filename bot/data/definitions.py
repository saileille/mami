"""Global variables are stored here to avoid circular import."""
CLIENT = None
ROOT_DIR = None
COMMANDS = None
LANGUAGES = {}
CACHE_LANGUAGE = None
DEFAULT_LANGUAGE_KEY_LOCATIONS = {}
GUILD_COMMAND_DATA = None
DEFAULT_COMMAND_DATA = None
USER_COMMAND_DATA = None
DATABASE_CONNECTION = None
DATABASE_CURSOR = None

DATA_CACHE = {"categories": {}, "channels": {}, "guilds": {}, "users": {}}
