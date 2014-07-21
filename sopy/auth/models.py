from flask import current_app, session
import requests
from sqlalchemy.ext.associationproxy import association_proxy
from sopy import db
from sopy.auth.login import UserMixin
from sopy.ext.models import IDModel
from sopy.se_data.models import SEUser


class Group(IDModel):
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name

        super(Group, self).__init__(**kwargs)

    def __str__(self):
        return self.name

    def compare_value(self):
        return self.name

    def get_unique(self, name, **kwargs):
        return super(Group, self).get_unique(name=name, **kwargs)


class User(UserMixin, SEUser):
    __tablename__ = 'user'

    id = db.Column(db.Integer, db.ForeignKey(SEUser.id), primary_key=True)
    superuser = db.Column(db.Boolean, nullable=False, default=False)

    _groups = db.relationship(Group, lambda: user_group, collection_class=set, backref=db.backref('users', collection_class=set))
    groups = association_proxy('_groups', 'name', creator=Group.get_unique)

    authenticated = True
    anonymous = False

    def has_group(self, group):
        if self.superuser:
            return True

        if isinstance(group, str):
            return group in self.groups

        return group in self._groups

    @classmethod
    def oauth_load(cls, token=None):
        r = requests.get('https://api.stackexchange.com/2.2/me', params={
            'key': current_app.config['SE_API_KEY'],
            'access_token': token or session['oauth_token'],
            'site': 'stackoverflow',
        })
        data = r.json()['items'][0]

        o = cls.get_unique(id=data['user_id'])

        return o.se_update(data)


user_group = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey(Group.id), primary_key=True)
)
