from wtforms import ValidationError
from flask.ext.wtf import Form
from wtforms.fields import StringField
from wtforms.validators import Required

from sopy.auth.models import User


class EditUserGroupsForm(Form):
    """ a form to add a user to a group """
    user_id = StringField('user id', validators=[Required()])

    def validate_user_id(self, field):
        """ check that the user ID exists in the db """
        if User.query.get(field.data) is None:
            raise ValidationError('No user with that ID exists')
