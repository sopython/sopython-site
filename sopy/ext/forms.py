import re
from flask import request
from wtforms import Field, Form as BaseForm, IntegerField, StringField
from wtforms.widgets import TextInput


class StripStringField(StringField):
    """String field that strips whitespace before validating."""

    def process_formdata(self, valuelist):
        self.data = valuelist[0].strip() if valuelist else ''

        if not self.data:
            self.raw_data = []


class SeparatedField(Field):
    widget = TextInput()

    def __init__(
        self, label=None, validators=None,
        pattern=r'(?:\s+|\s*,\s*)+', separator=' ',
        collection=set, sort=lambda x: x.lower(), getter=None,
        **kwargs
    ):
        super(SeparatedField, self).__init__(label, validators, **kwargs)
        self.pattern = re.compile(pattern)
        self.separator = separator
        self.collection = collection
        self.sort = sort
        self.getter = getter

    def _value(self):
        if not self.data:
            return ''

        data = (str(x) for x in self.collection(self.data))

        if self.sort is True:
            data = sorted(data)
        elif self.sort is not False:
            data = sorted(data, key=self.sort)

        return self.separator.join(data)

    def process_data(self, value):
        if value is None:
            self.data = value
        elif self.getter is None:
            self.data = self.collection(value)
        else:
            self.data = self.collection(self.getter(x) for x in value)

    def process_formdata(self, valuelist):
        raw = valuelist[0].strip() if valuelist else ''

        if not raw:
            self.data = self.collection()
            self.raw_data = []
            return

        items = self.pattern.split(raw)

        if not items:
            self.data = self.collection()
            return

        data = self.collection(x.strip() for x in items)

        if self.sort is True:
            self.data = sorted(data)
        elif self.sort is not False:
            self.data = sorted(data, key=self.sort)
        else:
            self.data = data


class PaginationForm(BaseForm):
    page = IntegerField(default=1)
    per_page = IntegerField(default=100)

    def __init__(self, formdata=None, *args, **kwargs):
        if formdata is None:
            formdata = request.args

        super(PaginationForm, self).__init__(formdata, *args, **kwargs)

    def validate_page(self, field):
        if field.data < 0:
            field.data = 0

    def validate_per_page(self, field):
        if field.data < 1 or field.data > 100:
            field.data = 100

    def apply(self, query):
        self.validate()

        return query.paginate(self.page.data, self.per_page.data)

    @classmethod
    def auto(cls, query):
        return cls().apply(query)
