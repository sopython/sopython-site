from collections import Mapping
from functools import wraps
from flask import render_template, url_for, redirect
import hoep as h
from markupsafe import Markup
from pygments import highlight
from pygments.formatters import get_formatter_by_name
import re
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


def template(path, **kwargs):
    """Render a template if the decorated view returns a context dictionary.

    If the view does not return a dictionary, the return value will be passed through.

    :param path: template to render
    :param kwargs: default context to pass to template, can be overridden by view context
    :return: view decorator
    """
    default_context = kwargs

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)

            if not isinstance(result, Mapping):
                return result

            context = default_context.copy()
            context.update(result)

            return render_template(path, **context)

        return inner

    return decorator


def redirect_for(endpoint, code=302, **values):
    return redirect(url_for(endpoint, **values), code)


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


def init_app(app):
    app.add_template_filter(markdown)


#TODO id_slug route processor accespts id/slug, ignores slug if not present
