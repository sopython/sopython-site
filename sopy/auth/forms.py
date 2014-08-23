from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired
from sopy.auth.models import User


class LoginForm(Form):
    user_id = StringField('User ID', validators=[InputRequired()])

    def validate_user_id(self, field):
        self.user = User.se_load(field.data)
