from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app.models import Post, User
from . import db

blog = Blueprint('blog', __name__, url_prefix='/')


@blog.route('/')
def index():
    posts = Post.query.all()
    users = User.query.all()
    # db.session.query(User).delete()
    # db.session.query(Post).delete()
    # db.session.commit()
    return render_template('blog/index.html', posts=posts, users=users)


@blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = current_user.id
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, content=content, author_id=author_id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@blog.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.filter_by(id=id).first()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post.title = title
        post.content = content
        db.session.commit()
        return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blog.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
