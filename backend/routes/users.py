from flask import Blueprint, request, jsonify
from models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .auth import check_user,check_admin
import bcrypt

engine = create_engine("sqlite:///../data.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

users_bp = Blueprint('users', __name__)

@users_bp.route("/all-users")
def get_all_users():
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        results = session.query(User).filter(User.active == True).all()
        users = [user.to_dict() for user in results]
        return jsonify(users)
    
    return jsonify({'error':'Forbidden'}), 403


@users_bp.route("/add-user", methods = ['POST'])
def add_user():
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        data = request.get_json()
        check_user_name = session.query(User).filter_by(user_name=data['user_name']).first()
        if check_user_name is not None:
            return jsonify({'error': 'Username already exists'}), 409
        hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(user_name = data['user_name'], user_email = data['user_email'], user_password=hashed_password)
        session.add(new_user)
        session.commit()
        return jsonify(new_user.to_dict()), 201
    
    return jsonify({'error':'Forbidden'}), 403


@users_bp.route("/update-user/<int:user_id>", methods = ['PUT'])
def update_user(user_id):
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        data = request.get_json()
        upd_user = session.query(User).filter(User.user_id == user_id).first()
        if upd_user is None:
            return jsonify({'error':'User not found'}), 404
        if 'user_name' in data and data['user_name'].strip():
            upd_user.user_name = data['user_name']
        if 'user_email' in data and data['user_email'].strip():
            upd_user.user_email = data['user_email']
        if 'user_password' in data and data['user_password'].strip():
            hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            upd_user.user_password = hashed_password
        session.commit()
        return jsonify(upd_user.to_dict()), 200

    return jsonify({'error':'Forbidden'}), 403


@users_bp.route("/make-admin/<int:user_id>", methods = ['PUT'])
def make_admin(user_id):
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        upd_user = session.query(User).filter(User.user_id == user_id).first()
        if upd_user is None:
            return jsonify({'error':'User not found'}), 404
        if upd_user.permission_level == 'A':
            return jsonify({'error': 'User allready admin'}), 409
        upd_user.permission_level = 'A'
        session.commit()
        return jsonify({'message': 'User premissions updated'}), 200
    
    return jsonify({'error':'Forbidden'}), 403


@users_bp.route("/remove-admin/<int:user_id>", methods = ['PUT'])
def remove_admin(user_id):
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        upd_user = session.query(User).filter(User.user_id == user_id).first()
        if upd_user is None:
            return jsonify({'error':'User not found'}), 404
        if upd_user.permission_level == 'U':
            return jsonify({'error': 'User allready not admin'}), 409
        upd_user.permission_level = 'U'
        session.commit()
        return jsonify({'message': 'User premissions updated'}), 200
    
    
    return jsonify({'error':'Forbidden'}), 403


@users_bp.route("/delete-user/<int:user_id>", methods = ['DELETE'])
def delete_user(user_id):
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        dlt_user = session.query(User).filter(User.user_id == user_id).first()
        if dlt_user is None:
            return jsonify({'error':'User not found'}), 404
        if dlt_user.active == False:
            return jsonify({'error': 'User allready deleted'}), 409
        dlt_user.active = False
        session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    
    return jsonify({'error':'Forbidden'}), 403

