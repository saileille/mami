"""Language-related conversion."""
from bot.misc import embed_messages


async def language_id(argument, context):
    """
    Check if the argument is a valid language name.

    If valid, return the language ID.
    """
    language = context.language
    for key in language.languages:
        if language.languages[key] == argument:
            return key

    custom_msg = await context.get_language_text("invalid_language")
    await embed_messages.invalid_argument(context, argument, custom_msg)

    return None
