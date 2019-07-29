"""Global variables are stored here to avoid circular import."""
CLIENT = None
ROOT_DIR = None
COMMANDS = None
LANGUAGES = {}
CACHE_LANGUAGE = None
DEFAULT_LANGUAGE_KEY_LOCATIONS = {}
GUILD_DEFAULT_COMMAND_RULES = None
EMPTY_COMMAND_RULES = None
DATABASE_CONNECTION = None
DATABASE_CURSOR = None

DATA_CACHE = {"categories": {}, "channels": {}, "guilds": {}, "users": {}}
