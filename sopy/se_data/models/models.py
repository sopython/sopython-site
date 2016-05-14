import re
from flask import current_app
import requests
from sopy import db
from sopy.ext.models import ExternalIDModel
from sopy.tags.models import HasTags

users_url = 'https://api.stackexchange.com/2.2/users/{}'
user_id_re = re.compile(r'/u(?:sers)?/(-?[0-9]+)')


class SEUser(ExternalIDModel):
    display_name = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String, nullable=False)
    profile_link = db.Column(db.String, nullable=False)
    reputation = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return '{} {}'.format(self.id, self.display_name)

    @classmethod
    def se_load(cls, ident, update=True):
        """Load a user by id.  If the user is not in the database, retrieve them with the API.

        If the same user may be (re-)cached multiple times in one operation, you can pass `update=False` to only retrieve the data from the API if the user hasn't been cached.

        :param ident: user id to load
        :param update: if False, an API call will only be made if this user hasn't been cached
        :return: user instance
        """

        try:
            id = int(ident)
        except ValueError:
            match = user_id_re.search(ident)
            id = int(match.group(1))

        o = cls.get_unique(id=id)

        # only update if told to or if the instance hasn't been cached
        if update or o.display_name is None:
            o.se_update()

        return o

    def se_update(self, data=None):
        if data is None:
            r = requests.get(users_url.format(self.id), params={
                'key': current_app.config.get('SE_API_KEY'),
                'site': 'stackoverflow',
            })
            items = r.json()['items']
            data = items[0] if items else False

        if data is False and self.display_name is None:
            # this user hasn't been cached, but can't be retrieved from the API
            # so create a dummy user
            self.display_name = 'user{}'.format(self.id)
            self.profile_image = ''
            self.profile_link = ''
            self.reputation = -1
        elif data:
            self.display_name = data['display_name']
            self.profile_image = data['profile_image']
            self.profile_link = data['link']
            self.reputation = data['reputation']

        return self


questions_url = 'https://api.stackexchange.com/2.2/questions/{}'
question_id_re = re.compile(r'/q(?:uestions)?/([0-9]+)')


class SEQuestion(HasTags, ExternalIDModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)

    @classmethod
    def se_load(cls, ident):
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
        r = requests.get(questions_url.format(id), params={
            'key': current_app.config.get('SE_API_KEY'),
            'site': 'stackoverflow',
            'filter': '!5RCKN561Hrx5Mj7Pc*qRTOUCj',
        })
        data = r.json()['items'][0]

        #TODO: error checking

        return o.se_update(data)

    def se_update(self, data=None):
        """Update question based on latest SO data.

        :param data: pre-requested data, or None to load the data now
        :return: updated instance
        """

        if data is None:
            r = requests.get(questions_url.format(self.id), params={
                'key': current_app.config.get('SE_API_KEY'),
                'site': 'stackoverflow',
                'filter': '!5RCKN561Hrx5Mj7Pc*qRTOUCj',
            })
            data = r.json()['items'][0]

        self.title = data['title']
        self.body = data['body_markdown']
        self.link = data['link']
        self.tags.update(data['tags'])

        return self
