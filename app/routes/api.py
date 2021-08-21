import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db

# defines the endpoints for the app
bp = Blueprint('api', __name__, url_prefix='/api')


# receives data
@bp.route('/users', methods=['POST'])
def signup():
    # captures the data like console.log in Node.js and Express.js
    data = request.get_json()
    print(data)
    # connects to database
    db = get_db()

    # try... except handles any errors
    try:
        # attempt to create a new user
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save in database
        # use db.add to prep the INSERT statement and the db.commit method to officially update the database
        db.add(newUser)
        db.commit()
    except:
        # print will print the error message in the powershell
        print(sys.exc_info()[0])

        # insert failed, so rollback and send error to front end, 500 is the status code
        # rollback() ensures that the database won't lock up when deployed to Heroku, prevents connection from remaining in a pending state resulting in app crashing
        db.rollback()
        return jsonify(message = 'Signup failed'), 500
       
    # clears any existing session data and creates two new session properties
    session.clear()
    # property 1 = aids future database queries
    session['user_id'] = newUser.id
    # property 2 = templates will use to conditionally render elements
    session['loggedIn'] = True

    #sends the front end JSON notation that includes the ID of the new user
    return jsonify(id = newUser.id)


@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    # returns 204 status which indicates there is no content
    return '', 204


@bp.route('/users/login', methods=['POST'])
def login():
    # connects to database
    data = request.get_json()
    db = get_db()

    # check whether user's posted email address exists in database
    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400
    
    # sends data['password'] as second parameter in verify_password method in User model, returns 400 status if password doesn't match
    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400

    # clears any existing session data and creates two new session properties
    session.clear()
    # property 1 = aids future database queries
    session['user_id'] = user.id
    # property 2 = templates will use to conditionally render elements
    session['loggedIn'] = True


    return jsonify(id = user.id)


@bp.route('/comments', methods=['POST'])
def comment():
    # connects to database
    data = request.get_json()
    db = get_db()

    try:
        # create a new comment
        newComment = Comment(
            # come from the front end thats why we use 'data'
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            # comes from the session which stores the user_id value, thats why we use session.get()
            user_id = session.get('user_id')
        )

        db.add(newComment)
        # performs the INSERT above against the database
        db.commit()
    except:
        print(sys.exc_info()[0])

        # rollback() discards the pending commit if it fails
        db.rollback()
        return jsonify(message = 'Comment failed'), 500

    # comment creation succeeded so return newly created ID
    return jsonify(id = newComment.id)


@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote failed'), 500

    return '', 204


@bp.route('/posts', methods=['POST'])
def create():
    data = request.get_json()
    db = get_db()

    try:
        # create a new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed'), 500

    return jsonify(id = newPost.id)

# updates the details of a post
@bp.route('/posts/<id>', methods=['PUT'])
# use id to perform the update
def update(id):
    data = request.get_json()
    db = get_db()

    try:
        #retrieve post and update title property
        #SQLAlchemy requires you to query the database for the corresponding record, update object like normal object, and then recommit it
        post = db.query(Post).filter(Post.id == id).one()
        # post is an object created from User class so use DOT NOTATION, whereas data is a dictionary so we use BRACKET NOTATION
        post.title = data['title']
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404

    return '', 204


@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
    # connects to db
    db = get_db()

    try:
        # delete post from db
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404

    return '', 204