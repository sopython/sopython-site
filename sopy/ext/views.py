from collections import Mapping
from functools import wraps
from flask import render_template, url_for, redirect
import hoep as h
from markupsafe import Markup


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


md = h.Hoep(
    h.EXT_AUTOLINK | h.EXT_FENCED_CODE | h.EXT_FOOTNOTES | h.EXT_HIGHLIGHT | h.EXT_SPACE_HEADERS | h.EXT_STRIKETHROUGH | h.EXT_SUPERSCRIPT | h.EXT_TABLES,
    h.HTML_HARD_WRAP | h.HTML_SMARTYPANTS | h.HTML_TOC
)
#TODO: add code highlighting


def markdown(text):
    return Markup(md.render(text))


def init_app(app):
    app.add_template_filter(markdown)
