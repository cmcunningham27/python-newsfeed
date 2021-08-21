from flask import Blueprint, request, jsonify
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

    # create a new user
    newUser = User(
        username = data['username'],
        email = data['email'],
        password = data['password']
    )

    # save in database
    # use db.add to prep the INSERT statement and the db.commit method to officially update the database
    db.add(newUser)
    db.commit()

    #sends the front end JSON notation that includes the ID of the new user
    return jsonify(id = newUser.id)