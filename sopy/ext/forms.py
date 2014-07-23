import re
from wtforms import Field
from wtforms.widgets import TextInput


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
        if not valuelist or not valuelist[0]:
            self.data = self.collection()
            return

        items = self.pattern.split(valuelist[0])

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
