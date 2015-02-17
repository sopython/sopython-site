from calendar import day_abbr, month_abbr
from datetime import date, time, datetime, timedelta
import re
import requests
from sopy import db
from sopy.ext.models import ExternalIDModel
from sopy.se_data.models import SEUser

full_text_url = 'http://chat.stackoverflow.com/messages/{}/{}'
id_re = re.compile(r'message-([\d]+)')
ts_re = re.compile(r"(?:(?:(?P<month>\w{3}) (?P<day>\d{1,2}) (?:'(?P<year>\d{2}) )?)|(?:(?P<weekday>\w{3}) ))?(?P<hour>\d{1,2}):(?P<minute>\d{2}) (?P<period>[AP]M)")
months = list(month_abbr)
days = list(day_abbr)


class ChatMessage(ExternalIDModel):
    room_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(SEUser.id), nullable=False)
    ts = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String, nullable=False)
    rendered = db.Column(db.Boolean, nullable=False)
    stars = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship(SEUser, backref='chat_messages')

    @classmethod
    def html_load(cls, element, room_id, ts_date=None, update=True):
        """Create a message by id and update it from scraped HTML.

        :param element: message element from Beautiful Soup
        :param room_id: needed for fetching "see full text" messages
        :param ts_date: date parsed from page containing message.  If None, the timestamps are assumed to have the full date, filling in missing fields with today's date.
        :return: instance
        """

        id = int(id_re.search(element['id']).group(1))
        o = cls.get_unique(id=id)

        if not update and o.ts is not None:
            return o

        o.room_id = room_id

        user_url = element.find_previous('div', class_='signature').find('a')['href']
        # don't try to re-cache existing users, since they may be loaded for multiple messages
        o.user = SEUser.se_load(ident=user_url, update=False)

        # Yam it, these are the dumbest timestamps ever.
        # Not every message in the transcript has a timestamp, so we just give all those messages the closest previous timestamp.
        # A timestamp can be:
        # hour:minute period, in which case you need the timestamp from the transcript page, or the current day if this is the starred message list
        # yst hour:minute period, in which case subtract one day
        # weekday hour:minute period, in which case treat today as the last day of the week to calculate and subtract an offset
        # month day hour:minute period, in which case you need to get the year from the transcript or the current day
        # month day 'year hour:minute period, hooray, the only thing wrong with this is the 2 digit year!
        # I know they have the full, seconds resolution, timestamp somewhere, because you can see it when hovering the timestamp in the recently starred list

        # if this is the transcript, the day was parsed and passed in, otherwise it's the chatroom and we start with the current date
        ts_date = ts_date if ts_date is not None else datetime.utcnow().date()
        # find the closest previous timestamp and parse it with a crazy regex to handle all the cases
        ts_data = ts_re.search(element.find_previous('div', class_='timestamp').string).groupdict()
        # at least there's always a time, instead of "5 minutes ago"
        hour = int(ts_data['hour'])
        minute = int(ts_data['minute'])

        if ts_data['month'] is not None:
            # there was a month, so this will replace the start date
            # if there's a year, use strptime to handle 2-digit years as sanely as possible
            # otherwise, use the date we started with to get the year
            year = datetime.strptime(ts_data['year'], '%y').year if ts_data['year'] is not None else ts_date.year
            # get a month's number by name
            month = months.index(ts_data['month'])
            day = int(ts_data['day'])
            # build the new date
            ts_date = date(year, month, day)
        elif ts_data['weekday'] is not None:
            # instead of the date, we got a day of the week in the starred list
            if ts_data['weekday'] == 'yst':
                # or even dumber, we got "yesterday"
                offset = timedelta(-1)
            else:
                # to figure out the offset for a given day relative to the current day
                # remember the days of the week start on monday and are zero based
                # go back 6 days
                # get the number for the day of the week
                # get the number for the current day of the week, treat that as the last day of the week by subtracting from 6
                # add the last day offset to the normal day number, wrapping around if we overflow the week
                offset = timedelta(-6 + ((days.index(ts_data['weekday']) + (6 - ts_date.weekday())) % 7))

            # modify today's date with the offset
            ts_date += offset

        if ts_data['period'] == 'AM' and hour == 12:
            # 12 AM is actually 0 in 24 hour time
            hour = 0
        elif ts_data['period'] == 'PM' and hour != 12:
            # hours after 12 PM are shifted up 12
            hour += 12

        # build a utc timestamp from the date and the time
        o.ts = datetime.combine(ts_date, time(hour, minute))

        if element.find(class_='partial') is not None:
            # this is a "see full text" message, load the full unrendered message
            o.content = requests.get(full_text_url.format(room_id, id)).text
            o.rendered = False
        else:
            # normal full message
            o.content = element.find('div', class_='content').decode_contents().strip()
            o.rendered = True

        stars_elem = element.find('span', class_='stars')
        o.stars = int(stars_elem.find('span', class_='times').string or 0) if stars_elem is not None else 0

        return o
