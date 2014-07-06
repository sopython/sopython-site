from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sopy import db
from sopy.ext.models import IDModel


class Tag(IDModel):
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name

        super(Tag, self).__init__(**kwargs)

    def __str__(self):
        return self.name

    def compare_value(self):
        return self.name

    @classmethod
    def get_unique(cls, name, **kwargs):
        return super(Tag, cls).get_unique(name=name, **kwargs)


class HasTags(object):
    @declared_attr
    def tag_assoc(cls):
        return db.Table(
            '{}_tag'.format(cls.__tablename__),
            db.Column('{}_id'.format(cls.__tablename__), db.ForeignKey('{}.id'.format(cls.__tablename__)), primary_key=True),
            db.Column('tag_id', db.ForeignKey(Tag.id), primary_key=True)
        )

    @declared_attr
    def _tags(cls):
        return db.relationship(Tag, lambda: cls.tag_assoc, collection_class=set)

    @declared_attr
    def tags(cls):
        return association_proxy('_tags', 'name', creator=Tag.get_unique)
