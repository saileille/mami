"""Language-related conversion."""
from bot.data import definitions
from bot.misc import embed_messages


async def language_id(argument, context):
    """
    Check if the argument is a valid language name or flag code.

    If valid, return the language ID.
    """
    language = context.language
    for key, lang_name in language.languages.items():
        if lang_name == argument:
            return key

    for key, lang_object in definitions.LANGUAGES.items():
        if argument in lang_object.flag_codes:
            return key

    custom_msg = await context.language.get_text("invalid_language")
    await embed_messages.invalid_argument(context, argument, custom_msg)

    return None
