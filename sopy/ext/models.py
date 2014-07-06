from sopy import db


class IDModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def __str__(self):
        return str(self.id)

    def compare_value(self):
        return self.id


class ExternalIDModel(IDModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
