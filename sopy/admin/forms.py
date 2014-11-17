from flask_wtf import Form
from wtforms.validators import ValidationError, InputRequired
from sopy import db
from sopy.auth.models import User
from sopy.ext.forms import StripStringField


class UserListForm(Form):
    user_ids = StripStringField('User IDs', validators=[InputRequired()])

    def validate_user_ids(self, field):
        raw_ids = field.data.split()
        int_ids = set()

        for id in raw_ids:
            try:
                int_ids.add(int(id))
            except TypeError:
                raise ValidationError('Invalid ID "{}"'.format(id))

        q_ids = db.session.query(db.cast(db.func.unnest(field.data.split()), db.Integer).label('id')).subquery()
        users = User.query.join((q_ids, q_ids.c.id == User.id)).all()
        new_ids = int_ids - {u.id for u in users}

        for id in new_ids:
            #TODO: use api to load multiple users in one request
            user = User.se_load(id)

            if user is None:
                raise ValidationError('Invalid ID "{}"'.format(id))

            users.append(user)

        self.users = users
