from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy, _camelcase_re, _QueryProperty, BaseQuery
from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta as BaseDeclarativeMeta, declared_attr, declarative_base
from sqlalchemy.orm import was_deleted


class EqMixin:
    """Compare and hash objects by custom values."""

    def compare_value(self):
        """Return what will be used to compare instances."""

        return inspect(type(self)).identity

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


class UniqueMixin:
    """Keep a cache of unique instances in memory so new instances can be safely created in bulk before they are committed."""

    @classmethod
    def get_unique(cls, **kwargs):
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
                o = cls(**kwargs)
                session.add(o)

            cache[key] = o

        return o


class DeclarativeMeta(BaseDeclarativeMeta):
    def __init__(cls, name, bases, attrs):
        """Handle Flask-SQLAlchemy's bind_key without setting tablename."""

        bind_key = attrs.pop('__bind_key__', None)
        BaseDeclarativeMeta.__init__(cls, name, bases, attrs)

        if bind_key is not None:
            cls.__table__.info['bind_key'] = bind_key


class Model(UniqueMixin, EqMixin):
    query_class = BaseQuery

    @declared_attr
    def __tablename__(cls):
        def _join(match):
            word = match.group()

            if len(word) > 1:
                return ('_%s_%s' % (word[:-1], word[-1])).lower()

            return '_' + word.lower()

        return _camelcase_re.sub(_join, cls.__name__).lstrip('_')

    def __str__(self):
        return str(inspect(self).identity)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self)

    def compare_value(self):
        return inspect(self).identity


class SQLAlchemy(BaseSQLAlchemy):
    def __init__(self, app=None, model=Model, meta=DeclarativeMeta, **kwargs):
        self.BaseModel = model
        self.DeclarativeMeta = meta
        super(SQLAlchemy, self).__init__(app, **kwargs)

    def init_app(self, app):
        super(SQLAlchemy, self).init_app(app)
        app.shell_context_processor(lambda: {'db': self})

    def make_declarative_base(self):
        metadata = MetaData(naming_convention={
            'pk': 'pk_%(table_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ix': 'ix_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
        })
        base = declarative_base(metadata=metadata, cls=self.BaseModel, name='Model', metaclass=self.DeclarativeMeta)
        base.query = _QueryProperty(self)
        base.db = self
        return base
