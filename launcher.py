"""Import stuff."""
import os

from bot.database import database_functions
from bot.data import definitions
from bot.data import initialisation
from bot.data import language_synchronisation
from bot.data import secrets
from framework.client import Client


def launch():
    """Launch the bot."""
    definitions.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    initialisation.initialise_commands()
    initialisation.initialise_languages()
    database_functions.connect()
    initialisation.update_config_data()
    language_synchronisation.synchronise()

    definitions.CLIENT = Client()
    definitions.CLIENT.run(secrets.BOT_TOKEN)


launch()
