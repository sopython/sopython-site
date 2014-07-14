from flask import url_for
from sopy import db
from sopy.ext.models import IDModel


class Salad(IDModel):
    term = db.Column(db.String, nullable=False, unique=True)
    definition = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.term

    def compare_value(self):
        return self.term

    @classmethod
    def get_unique(cls, term, **kwargs):
        return super(Salad, cls).get_unique(term=term, **kwargs)

    @property
    def update_url(self):
        return url_for('salad.update', id=self.id)

    @property
    def delete_url(self):
        return url_for('salad.delete', id=self.id)
