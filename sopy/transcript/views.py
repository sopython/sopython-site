import requests
import bs4
from datetime import date, timedelta

from sopy.transcript import bp
from sopy.ext.views import template

transcript_url = 'http://chat.stackoverflow.com/transcript/6/{year}/{month}/{day}/0-24'
today = date.today()
day = timedelta(days=1)

# d = date(year=2010, month=10, day=15)
d = date(year=2014, month=9, day=11)

def parse_monologue(mono):
    user_id = int(mono['class'][-1].split('-')[-1])
    user_name = mono.find(attrs={'class':'username'}).text
    out = []
    for message in mono.findAll(attrs={'class':'message'}):
        m = dict(user_id=user_id, user_name=user_name, date=d)
        m['id'] = int(message['id'].split('-')[-1])
        m['message'] = str(message.find(attrs={'class':'content'}))[22:-7].strip()
        out.append(m)
    return out

@bp.route('/')
@template('transcript/index.html')
def index():

    d = date(year=2014, month=9, day=11)
    messages = []

    while d < today:
        r = requests.get(transcript_url.format(day=d.day, month=d.month, year=d.year))
        soup = bs4.BeautifulSoup(r.text)
        transcript = soup.find('div', {'id':'transcript'})
        messages.extend([message for monologue in transcript.findAll(attrs={'class':'monologue'})
                    for message in parse_monologue(monologue)])

        d += day

    print(messages[:10])

    return {'messages':messages}
