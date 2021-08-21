#part of Python's built-in os module
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

#calling load_dotenv from python-dotenv since we used .env file
load_dotenv()

#connect to database using env variable
#manages the overall connection to database
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
#generates temporary connections for performing CRUD operations
Session = sessionmaker(bind=engine)
#helps us map the models to real MySQL tables
Base = declarative_base()

# app gets sent in through the app/__init__.py
def init_db(app):
    Base.metadata.create_all(engine)

    # runs close_db() with its built-in teardown_appcontext() method
    app.teardown_appcontext(close_db)

# saves the current connection on the g object if not already there, then returns connection from the g object instead of creating a new Session instance each time
def get_db():
    if 'db' not in g:
        # store db connection in app context
        g.db = Session()

    return g.db

# needs to be called above
def close_db(e=None):
    # attempts to find and remove db from the g object
    db = g.pop('db', None)

    # if db exists (db doesn't equal None) then end the connection
    if db is not None:
        db.close()