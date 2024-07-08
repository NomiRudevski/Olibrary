from sqlalchemy import create_engine
from flask import Flask
from flask_session import Session
from sqlalchemy.orm import sessionmaker
from .models import *



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'njf74^&*^ndk'

# Configure SQLAlchemy engine
engine = create_engine("sqlite:///../data.db", echo=True)
Base.metadata.bind = engine

# Configure session
Session(app)

# Optional: Configure upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create SQLAlchemy session
SQL_Session = sessionmaker(bind=engine)
SQL_session = SQL_Session()

# Ensure database tables are created
Base.metadata.create_all(engine)
