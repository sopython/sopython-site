from collections import Mapping
from functools import wraps
from flask import render_template, url_for, redirect


def template(path, **kwargs):
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
