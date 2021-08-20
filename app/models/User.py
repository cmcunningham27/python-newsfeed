from app.db import Base
#import classes from sqlalchemy module to define table columns and their data types
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

# create a salt to hash passwords against
salt = bcrypt.gensalt()

# User class inherits from Base class which was created in the db package, in order to declare several properties the parent Base will use to make the table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    @validates('email')
    # add validate_email method to class
    def validate_email(self, key, email):
        #make sure email address contains @ character, assert automatically throws error if condition is false preventing the return statement from happening.
        assert '@' in email

        return email

    @validates('password')
    def validate_password(self, key, password):
        # checks length of password and throws error if it has fewer then four characters
        assert len(password) > 4

        # returns encrypted version of the password
        return bcrypt.hashpw(password.encode('utf-8'), salt)