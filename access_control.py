from functools import wraps
from flask import flash, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if 'logged_in' in session:
        return f(*args, **kwargs)
      else:
        flash("ログインして続行してください", "danger")
        return redirect(url_for("login"))
    return decorated_function
    
def for_guests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if not 'logged_in' in session:
        return f(*args, **kwargs)
      else:
        flash("不正な実行です", "danger")
        return redirect(url_for("user_todo"))
    return decorated_function
