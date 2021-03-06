from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    # get all posts
    # function returns a session connection that's tied to this route's context
    db = get_db()
    # use query method on connection (db) to query Post model for all posts in descending order and we save the results in posts variable
    posts = db.query(Post).order_by(Post.created_at.desc()).all()

    #renders the template with posts data
    return render_template(
        'homepage.html',
        posts=posts,
        # passes the loggedIn session to the template
        loggedIn=session.get('loggedIn')
    )

# sends user to appropriate places based off of whether they are logged in or not
@bp.route('/login')
def login():
    # not logged in yet
    if session.get('loggedIn') is None:
        return render_template('login.html')

    return redirect('/dashboard')

@bp.route('/post/<id>')
def single(id):
    # get single post by id
    db = get_db()
    # use filter() to specify the SQL WHERE clause, and by using the one() instead of all()
    post = db.query(Post).filter(Post.id == id).one()

    # render single post template
    return render_template(
        # send single post to the template
        'single-post.html',
        post=post,
        # passes the loggedIn session to the template
        loggedIn=session.get('loggedIn')
        # once template is rendered and the response sent, the context for this route terminates, and the teardown function closes the database connection
    )