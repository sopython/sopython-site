from base64 import urlsafe_b64encode, urlsafe_b64decode
from flask import render_template, url_for
from sopy.spoiler import bp
from sopy.spoiler.forms import SpoilerForm


@bp.route('/', methods=['GET', 'POST'])
def encode():
    form = SpoilerForm(csrf_enabled=False)

    if form.validate_on_submit():
        message = form.message.data
        encoded = urlsafe_b64encode(message.encode('utf8')).decode('utf8')
        url = url_for('.decode', encoded=encoded, _external=True)
        return render_template('spoiler/encode.html', form=form, encoded=encoded, message=message, url=url)

    return render_template('spoiler/encode.html', form=form)


@bp.route('/<path:encoded>')
def decode(encoded):
    message = urlsafe_b64decode(encoded).decode('utf8')
    return render_template('spoiler/decode.html', encoded=encoded, message=message)
