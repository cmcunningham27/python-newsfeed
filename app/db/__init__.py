#part of Python's built-in os module
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

#calling load_dotenv from python-dotenv since we used .env file
load_dotenv()

#connect to database using env variable
#manages the overall connection to database
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
#generates temporary connections for performing CRUD operations
Session = sessionmaker(bind=engine)
#helps us map the models to real MySQL tables
Base = declarative_base()