from flask import url_for
from sopy import db
from sopy.ext.models import IDModel


class Salad(IDModel):
    term = db.Column(db.String, nullable=False, unique=True)
    definition = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=lambda: db.session.query(db.func.count(Salad.id) + 1).scalar())

    def __str__(self):
        return self.term

    def compare_value(self):
        return self.term

    def move_up(self):
        above = Salad.query.filter(Salad.position == self.position - 1).first()

        if above is not None:
            above.position += 1
            self.position -= 1

    def move_down(self):
        below = Salad.query.filter(Salad.position == self.position + 1).first()

        if below is not None:
            below.position -= 1
            self.position += 1

    def delete(self):
        below = Salad.query.filter(Salad.position > self.position).all()

        for item in below:
            item.position -= 1

        db.session.delete(self)

    @property
    def update_url(self):
        return url_for('salad.update', id=self.id)

    @property
    def move_up_url(self):
        return url_for('salad.move_up', id=self.id)

    @property
    def move_down_url(self):
        return url_for('salad.move_down', id=self.id)

    @property
    def delete_url(self):
        return url_for('salad.delete', id=self.id)
