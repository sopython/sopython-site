def load_previous(current):
    """Parse the page for the previous time block or day.

    :param current: current page
    :return: previous page
    """

    pass


def load_next(current):
    """Parse the page for the next time block or day.

    :param current: current page
    :return: next page
    """

    pass


def find_timestamp(message, page):
    """Find the closest timestamp for the given message.

    Works backwards until a message with a timestamp is found, potentially loading previous pages.

    :param message: parsed message
    :param page: whole page containing message
    :return: closest previous timestamp
    """

    pass


def get_range(start_id, end_id):
    """Get all messages between the start and end ids, inclusive.

    :param start_id: id of first message in range
    :param end_id: id of last message in range
    :return: list of parsed messages
    """

    pass
