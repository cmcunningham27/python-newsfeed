import sys
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

# defines the endpoints for the app
bp = Blueprint('api', __name__, url_prefix='/api')

# receives data
@bp.route('/users', methods=['POST'])
def signup():
    # captures the data like console.log in Node.js and Express.js
    data = request.get_json()
    print(data)
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