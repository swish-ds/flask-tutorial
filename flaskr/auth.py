# Blueprint
# way to organize a group of related views and other code
# Rather than registering views and other code directly with an application, they are registered with a blueprint. 
# blueprint is registered with the application when it is available in the factory function.

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') # The url_prefix will be prepended to all the URLs associated with the blueprint.

@bp.route('/register', methods=('GET', 'POST')) # When Flask receives a request to /auth/register, it will call the register view and use the return value as the response.
def register():
    # view function
    # this view will return HTML with a form for users to fill out
    # When they submit the form, it will create the new user and go to the login page.

    if request.method == 'POST': # If the user submitted the form, request.method will be 'POST'
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # url_for() generates the URL to a view based on a name and arguments. 
                # The name associated with a view is also called the endpoint
                # by default it’s the same as the name of the view function.
                # When using a blueprint, the name of the blueprint is prepended to the name of the function
                # endpoint for the login function is 'auth.login' because we added it to the 'auth' blueprint.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id'] # user’s id is stored in the session, it will be available on subsequent requests.
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request # registers a function that runs before the view function
def load_logged_in_user():
    # At the beginning of each request, if a user is logged in their information should be loaded and made available to other views.
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None # lasts for the length of the request
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    # remove the user id from the session
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    # Creating, editing, and deleting blog posts will require a user to be logged in
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        # If a user is loaded the original view is called and continues normally
        return view(**kwargs)

    return wrapped_view
