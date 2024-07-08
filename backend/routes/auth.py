from flask import Blueprint, request, jsonify, session, send_from_directory
from models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import bcrypt
from app import UPLOAD_FOLDER

engine = create_engine("sqlite:///../data.db", echo=True)
SQL_Session = sessionmaker(bind=engine)
SQL_session = SQL_Session()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods = ['POST'])
def register():
    data = request.get_json()
    check_user_name = SQL_session.query(User).filter_by(user_name=data['user_name']).first()
    if check_user_name is not None:
        return jsonify({'error': 'Username already exists'}), 409
    hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(user_name = data['user_name'], user_email = data['user_email'], user_password=hashed_password)
    SQL_session.add(new_user)
    SQL_session.commit()
    session["name"] = new_user.user_name
    return jsonify(new_user.to_dict()), 201

@auth_bp.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    user = SQL_session.query(User).filter(User.user_name == data['user_name']).first()
    if user is None:
        print("username")
        return jsonify({'error':'Log in details incorrect'}), 401
    if bcrypt.checkpw(data['user_password'].encode('utf-8'), user.user_password.encode('utf-8')) and user.active == True:
        session["name"] = user.user_name
        return jsonify({'message': 'Logged in successfully'}), 200

    return jsonify({'error': 'Log in details incorrect'}), 401

@auth_bp.route("/logout")
def logout():
    session["name"] = None
    return jsonify({'massege' : 'Loged out successfully'}), 200

@auth_bp.route("/check-admin")
def check_admin():
    user = SQL_session.query(User).filter(User.user_name == session.get("name")).first()
    if user.permission_level == 'A':
        return jsonify({'user_permission' : True})
    return jsonify({'user_permission' : False})


@auth_bp.route("/me")
def me():
    if not session.get("name"):
        return jsonify({'error':'Unauthorized'}), 401
    user = SQL_session.query(User).filter(User.user_name == session.get("name")).first()
    return jsonify(user.to_dict()), 200

@auth_bp.route('/images/<filename>')
def images(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def check_user():
    if not session.get("name"):
        return False
    user = SQL_session.query(User).filter(User.user_name == session.get("name")).first()
    return user

def check_admin(user):
    if user.permission_level == 'A':
        return True
    return False