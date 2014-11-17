from flask_wtf import Form
from wtforms.validators import InputRequired
from sopy.auth.models import User
from sopy.ext.forms import StripStringField


class LoginForm(Form):
    user_id = StripStringField('User ID', validators=[InputRequired()])

    def validate_user_id(self, field):
        self.user = User.se_load(field.data)
