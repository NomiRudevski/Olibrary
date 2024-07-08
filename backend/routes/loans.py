from flask import Blueprint, request, jsonify
from models import Loan, Book
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from .auth import check_admin, check_user

engine = create_engine("sqlite:///../data.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

loans_bp = Blueprint('loans', __name__)


@loans_bp.route("/all-loans")
def get_all_loans():
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        results = session.query(Loan).filter(Loan.active == True).all()
        loans = [loan.to_dict() for loan in results]
        return jsonify(loans), 200
    
    return jsonify({'error':'Forbidden'}), 403

@loans_bp.route("/late-loans")
def get_all_late_loans():
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    results = session.query(Loan, Book).join(Book, Loan.book_id == Book.book_id).filter(Loan.user_id == user.user_id, Loan.active == True, Loan.is_late == True).all()
    loans = [book.to_dict() for loan, book in results]

    return jsonify(loans), 200

@loans_bp.route("/user-loans")
def get_user_loans():
    user = check_user()
    if not user:
        return jsonify({'error': 'Log in to continue'}), 401
    
    results = session.query(Loan, Book).join(Book, Loan.book_id == Book.book_id).filter(Loan.user_id == user.user_id, Loan.active == True).all()
    loans = [{
        **book.to_dict(),
        'is_late': loan.is_late,
        'loan_id': loan.loan_id
    } for loan, book in results]

    return jsonify(loans), 200



@loans_bp.route("/create-loan", methods = ['POST'])
def create_loan():
    data = request.get_json()
    book_id = data['book_id']
    book = session.query(Book).filter(Book.book_id == book_id).first()
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if book is None or  book.is_loand == True or book.active == False:
        return jsonify({'error' : 'Book not available'}), 400
    
    loan_date = datetime.now().strftime('%Y-%m-%d')
    loan_duration = book.loan_type
    future_date = datetime.now() + timedelta(days=loan_duration)
    return_date = future_date.strftime('%Y-%m-%d')
    
    user_id = user.user_id
    new_loan = Loan(user_id = user_id, book_id = book_id, loan_date = loan_date, return_date = return_date)
    session.add(new_loan)
    
    book.is_loand = True
    session.commit()
    return jsonify(new_loan.to_dict()), 201


@loans_bp.route("/return-book/<int:loan_id>")
def deactivate_loan(loan_id):
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    loan = session.query(Loan).filter(Loan.loan_id == loan_id).first()
    book = session.query(Book).filter(Book.book_id == loan.book_id).first()
    if loan is None:
        return jsonify({'error':'Loan not found'}), 404
    if loan.active == False:
        return jsonify({'error': 'Book allready returned'}), 409
    loan.active = False
    book.is_loand = False
    session.commit()
    return jsonify({'massege': 'Book returned successfully'}), 200


@loans_bp.route("/extend-loan/<int:loan_id>")
def extend_loan(loan_id):
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    loan = session.query(Loan).filter(Loan.loan_id == loan_id).first()
    if loan is None:
        return jsonify({'error':'Loan not found'}), 404
    if loan.active == False:
        return jsonify({'error': 'Book allready returned'}), 409
    if loan.is_late == True:
        return jsonify({'error':'Unable to extend the loan period of a late book'}), 409
    
    curent_return_date = loan.return_date
    date_object = datetime.strptime(curent_return_date, '%Y-%m-%d')
    extended_date = date_object + timedelta(days=10)
    new_return_date = extended_date.strftime('%Y-%m-%d')

    loan.return_date = new_return_date
    session.commit()
    return jsonify({'massege': 'Loan period extended successfully'}), 200


@loans_bp.route("/cheak-if-late")
def cheak_late_books():
    today = datetime.now().date()
    results = session.query(Loan).filter(Loan.active == True).all()
    for loan in results:
        return_date = datetime.strptime(loan.return_date, '%Y-%m-%d').date()
        if today > return_date:
            loan.is_late = True
    session.commit()
    return '', 204

