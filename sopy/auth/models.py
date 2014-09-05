from flask import current_app, session
import requests
from sqlalchemy.ext.associationproxy import association_proxy
from sopy import db
from sopy.auth.login import UserMixin
from sopy.ext.models import IDModel
from sopy.se_data.models import SEUser


class Group(IDModel):
    name = db.Column(db.String, nullable=False, unique=True)

    _groups = db.relationship(
        lambda: Group, lambda: group_group,
        primaryjoin=lambda: Group.id == group_group.c.member_id,
        secondaryjoin=lambda: Group.id == group_group.c.group_id,
        collection_class=set,
        backref=db.backref('_members', collection_class=set)
    )
    groups = association_proxy('_groups', 'name', creator=lambda x: Group.get_unique(x))
    members = association_proxy('_members', 'name', creator=lambda x: Group.get_unique(x))

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name

        super(Group, self).__init__(**kwargs)

    def __str__(self):
        return self.name

    def compare_value(self):
        return self.name

    @classmethod
    def get_unique(cls, name, **kwargs):
        return super(Group, cls).get_unique(name=name, **kwargs)

    def has_group(self, *groups):
        for group in groups:
            if isinstance(group, str):
                if group in self.groups:
                    return True

            if group in self._groups:
                return True

        return any(sub.has_group(*groups) for sub in self._groups)


group_group = db.Table(
    'group_group',
    db.Column('member_id', db.Integer, db.ForeignKey(Group.id), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey(Group.id), primary_key=True)
)


class User(UserMixin, SEUser):
    __tablename__ = 'user'

    id = db.Column(db.Integer, db.ForeignKey(SEUser.id), primary_key=True)
    superuser = db.Column(db.Boolean, nullable=False, default=False)

    _groups = db.relationship(
        Group, lambda: user_group, collection_class=set,
        backref=db.backref('users', collection_class=set)
    )
    groups = association_proxy('_groups', 'name', creator=Group.get_unique)

    authenticated = True
    anonymous = False

    def has_group(self, *groups):
        if self.superuser:
            return True

        for group in groups:
            if isinstance(group, str):
                if group in self.groups:
                    return True

            if group in self._groups:
                return True

        return any(sub.has_group(*groups) for sub in self._groups)

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
