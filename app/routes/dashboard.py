from flask import Blueprint, render_template, session
from app.models import Post
from app.db import get_db
# imports decorator login_required
from app.utils.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
# decorators must go between the route() and the function
@login_required
def dash():
    # connects to db
    db = get_db()

    # query post information
    posts = (
        db.query(Post)
        .filter(Post.user_id == session.get('user_id'))
        .order_by(Post.created_at.desc())
        .all()
    )

    return render_template(
        'dashboard.html',
        posts=posts,
        loggedIn=session.get('loggedIn')
    )

@bp.route('/edit/<id>')
@login_required
def edit(id):
    # get single post by id
    db = get_db()
    post = db.query(Post).filter(Post.id == id).one()

    # render edit page
    return render_template(
        'edit-post.html',
        post=post,
        loggedIn=session.get('loggedIn')
    )