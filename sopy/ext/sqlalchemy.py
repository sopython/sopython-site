from datetime import datetime

from flask import current_app, g
from flask_alembic import Alembic
from flask_sqlalchemy import Model as BaseModel, SQLAlchemy as BaseSQLAlchemy
from sqlalchemy import MetaData, inspect
from sqlalchemy.orm import was_deleted


class Model(BaseModel):
    def compare_value(self):
        """Return what will be used to compare instances."""
        return inspect(self).identity

    def __eq__(self, other):
        """Instances of same class with equal compare values are equal."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.compare_value() == other.compare_value()

    def __ne__(self, other):
        eq = self.__eq__(other)

        if eq is NotImplemented:
            return eq

        return not eq

    def __hash__(self):
        """Composite hash of class and compare value."""
        return hash(self.__class__) ^ hash(self.compare_value())

    @classmethod
    def create_unique(cls, session, **kwargs):
        o = cls(**kwargs)
        session.add(o)
        return o

    @classmethod
    def get_unique(cls, **kwargs):
        """Keep a cache of unique instances in memory so new instances
        can be safely created in bulk before they are committed.
        """
        g._unique_cache = cache = getattr(g, '_unique_cache', {})
        key = (cls, tuple(kwargs.items()))
        o = cache.get(key)

        if o is not None and was_deleted(o):
            o = None

        if o is None:
            session = current_app.extensions['sqlalchemy'].db.session

            with session.no_autoflush:
                o = session.query(cls).filter_by(**kwargs).first()

            if o is None:
                o = cls.create_unique(session, **kwargs)

            cache[key] = o

        return o


def rev_id():
    offset = datetime(2017, 12, 13, 21)
    now = datetime.utcnow()
    return str(int((now - offset).total_seconds()))


class SQLAlchemy(BaseSQLAlchemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alembic = Alembic()
        self.alembic.rev_id = rev_id

    def init_app(self, app):
        super(SQLAlchemy, self).init_app(app)
        self.alembic.init_app(app)
        app.shell_context_processor(lambda: {'db': self})


db = SQLAlchemy(
    metadata=MetaData(naming_convention={
        'pk': 'pk_%(table_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ix': 'ix_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }),
    model_class=Model
)
