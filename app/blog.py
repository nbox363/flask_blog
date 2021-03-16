from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from sqlalchemy.exc import OperationalError

from app.models import Post, User, Comment
from . import db

blog = Blueprint('blog', __name__, url_prefix='/')


@blog.route('/')
def index():
    try:
        posts = Post.query.all()
        users = User.query.all()
        return render_template('blog/index.html', posts=posts, users=users)
    except OperationalError:
        return render_template('blog/index.html')
    # db.session.query(User).delete()
    # db.session.query(Post).delete()
    # db.session.commit()



@blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
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
        title = request.form.get('title')
        content = request.form.get('content')
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


@blog.route('/<int:id>', methods=['POST', 'GET'])
@login_required
def post_detail(id):
    comments = Comment.query.filter_by(post_id=id)
    post = Post.query.filter_by(id=id).first()
    users = User.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        new_comment = Comment(post_id=id, author_id=current_user.id, title=title, content=content)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('blog.post_detail', id=id))

    return render_template('blog/post_detail.html', post=post, comments=comments, users=users)


@blog.route('/<int:id>/update_comment', methods=('GET', 'POST'))
@login_required
def update_comment(id):
    comment = Comment.query.filter_by(id=id).first()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        comment.title = title
        comment.content = content
        db.session.commit()
        return redirect(url_for('blog.post_detail', id=comment.post_id))

    return render_template('blog/update_comment.html', comment=comment)


@blog.route('/<int:id>/delete_comment', methods=('GET', 'POST'))
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog.post_detail', id=comment.post_id))