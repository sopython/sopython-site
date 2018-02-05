from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from sopy.auth.models import User
from sopy.ext.forms import StripStringField


class LoginForm(FlaskForm):
    user_id = StripStringField('User ID', validators=[InputRequired()])

    def validate_user_id(self, field):
        self.user = User.se_load(field.data)
