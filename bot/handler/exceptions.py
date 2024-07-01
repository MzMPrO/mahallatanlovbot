import logging
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)


async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        return True

    if isinstance(exception, MessageNotModified):
        return True
    if isinstance(exception, MessageCantBeDeleted):
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        return True

    if isinstance(exception, MessageTextIsEmpty):
        return True

    if isinstance(exception, Unauthorized):
        return True

    if isinstance(exception, InvalidQueryID):
        return True

    if isinstance(exception, TelegramAPIError):
        return True
    if isinstance(exception, RetryAfter):
        return True
    if isinstance(exception, CantParseEntities):
        return True
