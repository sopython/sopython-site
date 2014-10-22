from collections import Mapping
from functools import wraps
from urllib.parse import urlparse, urljoin
from flask import render_template, url_for, redirect, request
import hoep as h
from inflection import parameterize
from markupsafe import Markup
from pygments import highlight
from pygments.formatters import get_formatter_by_name
import re
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from werkzeug.routing import BaseConverter


def template(path=None, **default_context):
    """Render a template if the decorated view returns a context dictionary.

    If the returned context includes the key '_template', that value is used as the template path.

    If the view does not return a dictionary, the return value will be passed through.

    :param path: template to render
    :param kwargs: default context to pass to template, can be overridden by view context
    :return: view decorator
    """
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)

            if not isinstance(result, Mapping):
                return result

            context = default_context.copy()
            context.update(result)

            template_path = context.pop('_template', path)

            if template_path is None:
                raise KeyError('No default template provided, and no template passed in context.')

            return render_template(template_path, **context)

        return inner

    return decorator


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

    Only the id is returned, the slug is dropped if present.  The id can be negative.  When building a url, pass in the
    model instance, not the id or slug.  By default the slug is generated from the string representation of the object.

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


def init_app(app):
    app.add_template_filter(markdown)
    app.url_map.converters['id_slug'] = IDSlugConverter
