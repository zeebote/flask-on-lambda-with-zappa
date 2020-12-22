from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
#from datetime import datetime
from flask_login import login_required, current_user
#from .auth import login_required
from .db import get_db
#from sqlalchemy.sql import text, func
from .models import Post, User
#from sqlalchemy import and_
#from sqlalchemy.sql import select
#from sqlalchemy.dialects import postgresql
#from flaskr.db import Base
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    #session = get_session()
    #j = Base.query.post.join(user, post.c.author_id == user.c.id)
    #stmt = select([post.id, title, body, created, author_id, username]).select_from(j)
    posts = db.execute(
         #'SELECT p.id, title, body, created, author_id, username'
         #' FROM post p JOIN user_tb u ON p.author_id = u.id'
         #' ORDER BY created DESC'
         '''SELECT user_tb.username, post.id, post.title, post.body, post.created, post.author_id
         FROM post, user_tb
         WHERE post.author_id = user_tb.id
         ORDER BY created DESC'''
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            #a_id = g.user.id
            #db = get_db()
            #db.execute(
            #    'INSERT INTO post (title, body, author_id)'
            #    ' VALUES (?, ?, ?)',
            #    (title, body, a_id)
            #)
            #db.commit()
            #p = Base.metadata.tables['post']
            #ins = p.insert()

            #ins = p.insert().values(author_id=g.user['id'], title=title, body=body, created=datetime.now())
            #get_db.execute(ins)
            #user = User.query.filter_by(username=g.user['username']).first()

            #p = Post(author_id=current_user.id, title=title, body=body, created=datetime.now())
            #db_session.add(p)
            #db_session.commit()
            
            db = get_db()
            #u_id = str(g.user['username'])
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (%s, %s, %s)', (title, body, current_user.id,)
            )
            #db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
    #post = db_session.execute(text(
        #'SELECT p.id, title, body, created, author_id, username'
        #' FROM post p JOIN user_tb u ON p.author_id = u.id'
        #' WHERE p.id = ?',
        #(id,)
        'SELECT post.id, post.title, post.body, post.created, post.author_id, user_tb.username'
        ' FROM post, user_tb'
        ' WHERE post.author_id = user_tb.id AND post.id = %s', (id) 
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != current_user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = %s, body=%s'
                ' WHERE id = %s', (title, body, id,)
                #'UPDATE post SET title = title, body = body'
                #' WHERE id = (%s)' % (id)
            )
            #db_session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = %s' % (id,))
    #db.commit()
    return redirect(url_for('blog.index'))
