from urllib.parse import urlparse, urljoin, quote
from flask import url_for, redirect, request
import hoep as h
from inflection import parameterize
from markupsafe import Markup
from pygments import highlight
from pygments.formatters import get_formatter_by_name
import re
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from werkzeug.routing import BaseConverter
from werkzeug.urls import Href
from sopy import __version__


def redirect_for(endpoint, code=302, **values):
    return redirect(url_for(endpoint, **values), code)


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.form.get('next'), request.args.get('next'), request.referrer:
        if not target:
            continue

        if is_safe_url(target):
            return target


def redirect_next(endpoint='index', **values):
    target = get_redirect_target()

    if not target:
        target = url_for(endpoint, **values)

    return redirect(target)


class SOMarkdown(h.Hoep):
    formatter = get_formatter_by_name('html', style='tango', noclasses=True)

    lang_re = re.compile(r'<!--\s?language(-all)?:\s?(?:lang-)?([\w\-]+)\s?-->', re.I)
    set_language = None
    set_language_persist = None

    default_lexer = get_lexer_by_name('python3')

    def block_code(self, text, language):
        """Highlight the code block using Pygments.

        To determine what lexer to use, checks the following in order:

        * Fenced block code (~~~python3)
        * <!-- language: python3 -->, above the block
        * <!-- language-all: python3 -->, for all subsequent blocks
        * The default language, python3

        The language code can have the optional "lang-" prefix.

        If the code is "default", the default language, python3, is used.

        If the code is "none", no highlighting is applied.

        :param text: code block to highlight
        :param language: language code from fenced block
        :return: highlighted code
        """
        if language and language.startswith('lang-'):
            language = language[5:]

        for language in (language, self.set_language, self.set_language_persist):
            if language == 'none':
                lexer = get_lexer_by_name('text')
                break

            if language == 'default':
                lexer = self.default_lexer
                break

            try:
                lexer = get_lexer_by_name(language)
                break
            except ClassNotFound:
                pass
        else:
            lexer = self.default_lexer

        self.set_language = None  # set_language is only valid for one block

        return highlight(text, lexer, self.formatter)

    def block_html(self, text):
        """Capture language codes from HTML comments.

        If a language code is present, record it for use in :meth:`block_code`.

        :param text: html block to check
        :return: unaltered html block
        """
        match = self.lang_re.search(text)

        if match:
            persist, language = match.groups()

            if persist is None:
                self.set_language = language
            else:
                self.set_language_persist = language

        return text


md = SOMarkdown(
    h.EXT_AUTOLINK | h.EXT_FENCED_CODE | h.EXT_FOOTNOTES | h.EXT_HIGHLIGHT | h.EXT_SPACE_HEADERS | h.EXT_STRIKETHROUGH | h.EXT_SUPERSCRIPT | h.EXT_TABLES,
    h.HTML_HARD_WRAP | h.HTML_SMARTYPANTS | h.HTML_TOC
)


def markdown(text):
    return Markup(md.render(text))


class IDSlugConverter(BaseConverter):
    """Matches an int id and optional slug, separated by "/".

    :param attr: name of field to slugify, or None for default of str(instance)
    :param length: max length of slug when building url
    """

    regex = r'-?\d+(?:/[\w\-]*)?'

    def __init__(self, map, attr=None, length=80):
        self.attr = attr
        self.length = int(length)

        super(IDSlugConverter, self).__init__(map)

    def to_python(self, value):
        id, slug = (value.split('/') + [None])[:2]

        return int(id)

    def to_url(self, value):
        raw = str(value) if self.attr is None else getattr(value, self.attr, '')
        slug = parameterize(raw)[:self.length].rstrip('-')

        return '{}/{}'.format(value.id, slug).rstrip('/')


class WikiTitleConverter(BaseConverter):
    """Matches words separated by spaces or underscores.

    When parsing the url, underscores are converted to spaces.
    When building the url, spaces are converted to underscores.
    """

    def to_python(self, value):
        return value.replace('_', ' ')

    def to_url(self, value):
        return quote(value.replace(' ', '_'))


def query_update(**kwargs):
    """Update the query string with new values.

    This is useful, for example, for updating the pagination for a search query.

    :param kwargs: items to add to the query
    :return: path with updated query
    """

    q = request.args.copy()

    # can't use update since that appends values to the multi-dict instead of replacing
    for key, value in kwargs.items():
        q[key] = value

    return Href(request.path)(q)


def view_context():
    return {
        'query_update': query_update,
        '__version__': __version__
    }


def init_app(app):
    app.url_map.converters['id_slug'] = IDSlugConverter
    app.url_map.converters['wiki_title'] = WikiTitleConverter
    app.add_template_filter(markdown)
    app.add_template_global(query_update)
    app.context_processor(view_context)
