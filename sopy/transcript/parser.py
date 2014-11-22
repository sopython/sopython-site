import re
from datetime import date
from bs4 import BeautifulSoup
import requests
from sopy.se_data.models import ChatMessage

base_url = 'http://chat.stackoverflow.com/{}'
permalink_url = 'http://chat.stackoverflow.com/transcript/message/{}'
room_id_re = re.compile(r'^/rooms/(\d+)/')
date_re = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})')


def previous_page(current):
    """Load either the previous time block or the previous day.

    :param current: current page
    :return: previous page
    """

    element = None
    pager = current.find('div', class_='pager')

    if pager is not None:
        # check for a previous time block
        element = pager.find('span', class_='current').previous_sibling

    if element is None:
        # no previous time block, check for a previous day
        element = current.find('link', rel='prev')

    if element is None:
        # already on the first page
        return None

    # get and parse the new page
    r = requests.get(base_url.format(element['href']))
    r.raise_for_status()
    return BeautifulSoup(r.content)


def next_page(current):
    """Load either the next time block or the next day.

    :param current: current page
    :return: next page
    """

    element = None
    pager = current.find('div', class_='pager')

    if pager is not None:
        # check for a next time block
        element = pager.find('span', class_='current').next_sibling

    if element is None:
        # no next time block, check for a next day
        element = current.find('link', rel='next')

    if element is None:
        # already on the last day
        return None

    # get and parse the new page
    r = requests.get(base_url.format(element['href']))
    r.raise_for_status()
    return BeautifulSoup(r.content)


def page_date(page):
    """Parse the date from a page title.

    :param page: page element
    :return: parsed date
    """

    return date(**{key: int(value) for key, value in date_re.search(page.title.string).groupdict().items()})


def get_range(start_id, end_id):
    """Get all messages between the start and end ids, inclusive.

    :param start_id: id of first message in range
    :param end_id: id of last message in range
    :return: generator yielding messages
    """

    if end_id < start_id:
        raise ValueError('end must come after start')

    # need to check that the range is in the same room, so fetch start and end pages
    r = requests.get(permalink_url.format(start_id))
    r.raise_for_status()
    page = BeautifulSoup(r.content)
    room_href = page.find('span', class_='room-name').a['href']
    r = requests.get(permalink_url.format(end_id))
    r.raise_for_status()
    end_page = BeautifulSoup(r.content)

    if room_href != end_page.find('span', class_='room-name').a['href']:
        raise ValueError('start and end are in different rooms')

    # no need to keep the end data around, it must be reloaded anyway during traversal
    del r, end_page

    # need room id for fetching "see full text" messages
    room_id = int(room_id_re.search(room_href).group(1))
    # need date to build full timestamp, transcript messages just have time
    ts_date = page_date(page)
    # get the first message to cache
    element = page.find('div', id='message-{}'.format(start_id))

    while True:
        # build a full message from the html
        out = ChatMessage.html_load(element, room_id, ts_date)
        yield out

        if out.se_id >= end_id:
            break

        # get the next message element on the page
        element = element.find_next('div', class_='message')

        # reached the last message on the page, load the next page
        if element is None:
            page = next_page(page)
            ts_date = page_date(page)
            element = page.find('div', class_='message')
