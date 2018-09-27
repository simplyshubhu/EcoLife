from flask import session, redirect, url_for
from functools import wraps


def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return redirect(url_for('entry_page'))
    return wrapper
