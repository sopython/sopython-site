import os
from flask import current_app
from sopy.ext.views import template, redirect_for
from sopy.pages import bp


def iter_pages():
    """Get all available pages from the current app's templates."""

    # get all templates under 'pages/'
    names = (path[6:] for path in current_app.jinja_env.list_templates() if path.startswith('pages/'))
    # split the extension, check if it's allowed
    names = (os.path.splitext(name) for name in names)
    names = (name for name, ext in names if ext in ('.html',))
    # ignore special templates
    names = (name for name in names if name not in ('base', 'index'))

    return names


@bp.route('/')
@template('pages/index.html')
def index():
    return {'names': sorted(iter_pages())}


# name: context function
page_contexts = {}


def register_context(name):
    """Register a function that will return extra context for a given page. ::

        @register_context('random')
        def random_context():
            return {'value': random.random()}

    :param name: page name
    :return: context function decorator
    """

    def decorator(func):
        page_contexts[name] = func

        return func

    return decorator


# alias: real name
page_aliases = {
    'etiquette': 'chatroom',
}


@bp.route('/<name>')
@template()
def page(name):
    name = page_aliases.get(name, name)

    # check that name is available and not protected
    if name not in iter_pages():
        return redirect_for('pages.index')

    context = {'_template': 'pages/{}.html'.format(name)}
    context.update(page_contexts.get(name, lambda: {})())

    return context
