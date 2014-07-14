import re
import requests
from sopy import db
from sopy.ext.models import ExternalIDModel
from sopy.tags.models import HasTags, Tag

#TODO: use an api key

questions_url = 'https://api.stackexchange.com/2.2/questions/{}'
questions_params = {
    'site': 'stackoverflow',
    'filter': '!5RCKN561Hrx5Mj7Pc*qRTOUCj',
}

question_id_re = re.compile(r'stackoverflow\.com/q(?:uestions)?/([0-9]+)')


class SOQuestion(HasTags, ExternalIDModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)

    @classmethod
    def so_load(cls, ident):
        """Load SO data given a question id or link.

        If the question exists in the local db, it will be updated, otherwise it will be created.

        :param ident: question id or link
        :return: instance populated loaded data
        """
        try:
            id = int(ident)
        except ValueError:
            match = question_id_re.search(ident)
            id = int(match.group(1))

        o = cls.get_unique(id=id)
        r = requests.get(questions_url.format(id), params=questions_params)
        items = r.json()['items']

        #TODO: error checking

        return o.so_update(items[0])

    def so_update(self, data=None):
        """Update question based on latest SO data.

        :param data: pre-requested data, or None to load the data now
        :return: updated instance
        """
        if data is None:
            r = requests.get(questions_url.format(self.id), params=questions_params)
            data = r.json()['items'][0]

        self.title = data['title']
        self.body = data['body_markdown']
        self.link = data['link']
        self.tags.update(data['tags'])

        return self
