from datetime import datetime
from flask_wtf import FlaskForm
from requests import RequestException
from wtforms.fields import StringField, DateTimeField, TextAreaField, IntegerField
from wtforms.validators import Optional, InputRequired
from sopy.transcript.parser import get_range


class CreateTranscriptForm(FlaskForm):
    title = StringField(validators=[InputRequired()])
    ts = DateTimeField('When', format='%Y-%m-%d %H:%M', validators=[Optional()])
    body = TextAreaField('Description')
    start = IntegerField(validators=[Optional()])
    end = IntegerField(validators=[Optional()])

    def validate(self):
        result = super().validate()
        ts = self.ts.data
        start = self.start.data
        end = self.end.data
        now = datetime.utcnow()

        if ts is None and start is None:
            self.ts.errors.append('Must specify either a future event time or a message range.')
            result = False

        if ts is not None and start is None and ts <= now:
            self.ts.errors.append('Event without messages must be in the future.')
            result = False

        if start is not None and end is None:
            self.end.errors.append('Must specify full range.')
            result = False

        if start and end:
            try:
                self.messages = list(get_range(start, end))
            except (ValueError, RequestException) as e:
                self.end.errors.append(e.args[0])
                result = False
        else:
            self.messages = None

        return result

    def populate_obj(self, obj):
        obj.title = self.title.data
        obj.body = self.body.data

        if self.messages:
            obj.messages = self.messages

        if self.ts.data:
            obj.ts = self.ts.data
        else:
            obj.ts = self.messages[0].ts


class UpdateTranscriptForm(FlaskForm):
    title = StringField(validators=[InputRequired()])
    ts = DateTimeField('When', format='%Y-%m-%d %H:%M', validators=[Optional()])
    body = TextAreaField('Description')

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        formdata = self.meta.wrap_formdata(self, formdata)
        super().process(formdata, obj, data, **kwargs)

        if formdata is not None:
            self.remove_ids = {int(key[7:]) for key in formdata if key.startswith('remove-')}

    def populate_obj(self, obj):
        obj.title = self.title.data
        obj.body = self.body.data

        if self.remove_ids:
            obj.messages = [message for message in obj.messages if message.id not in self.remove_ids]

        if self.ts.data:
            obj.ts = self.ts.data
        else:
            obj.ts = obj.messages[0].ts
