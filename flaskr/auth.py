import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

#from sqlalchemy.sql import func
from flask_login import login_user, logout_user, login_required
from .models import User
from .db import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #reg = User.query.filter_by(username='fusername').first()
        #db = get_db()
        #session = get_session()
        user = User.query.filter_by(username=username.lower()).first()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif user:
            error = 'User {} is already registered.'.format(username)
            #return redirect(url_for('auth.register'))
        #elif session.execute(text(
        #    'SELECT id FROM user_tb WHERE username = ?', (fusername),)
        #).fetchone() is not None:
        #elif User.query.filter_by(username=username.lower()).first() is not None:
        #    error = 'User {} is already registered.'.format(username)
        #    return redirect(url_for('auth.register'))
        if error is None:
            #db.execute(text(
            #    'INSERT INTO user_tb (username, password) VALUES (?, ?)',
            #    (fusername, generate_password_hash(fpassword))
            #))
            #db.commit()
            new_user = User(username.lower(), generate_password_hash(password))
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #db = get_db()
        error = None
        #user = db.execute(text(
        #    'SELECT * FROM user_tb WHERE username = fusername')
        #).fetchone()
        user = User.query.filter_by(username=username).first() 
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            #session.clear()
            #session['user_id'] = user.id
            login_user(user, remember=True)

            #flash('Logged in successfully.')
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#@bp.before_app_request
#def load_logged_in_user():
#    user_id = session.get('user_id')

#    if user_id is None:
#        g.user = None
#    else:
        #g.user = user_id
#        g.user = User.query.filter_by(id=user_id).first()
        #g.user = get_db().execute(text(
        #    'SELECT * FROM user_tb WHERE id = ?', (user_id,)
        #)).fetchone()
        #g.user = User.query.filter_by(id='user_id')
@bp.route('/logout')
def logout():
    #session.clear()
    logout_user()
    return redirect(url_for('index'))
