from flask import Blueprint, request, jsonify
from models import Book
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .auth import check_user,check_admin
import os
from app import UPLOAD_FOLDER

engine = create_engine("sqlite:///../data.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

books_bp = Blueprint('books', __name__)

@books_bp.route("/all-books")
def get_all_books():
    results = session.query(Book).filter(Book.active == True).all()
    books = [book.to_dict() for book in results]
    return jsonify(books)


@books_bp.route("/available-books")
def get_available_books():
    results = session.query(Book).filter(Book.active == True, Book.is_loand == False).all()
    books = [book.to_dict() for book in results]
    return jsonify(books)

@books_bp.route("/book/<int:book_id>")
def get_book(book_id):
    book = session.query(Book).filter(Book.book_id == book_id, Book.active == True).first()
    if book:
        return jsonify(book.to_dict())
    else:
        return jsonify({"error": "Book not found"}), 404

@books_bp.route("/add-book", methods= ['POST'])
def add_book():
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):

        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
        else:
            filename = None

        data = request.form.to_dict()
        new_book = Book(title=data['title'], author=data['author'],description = data['description'], category = data['category'],loan_type = data['loan_type'] , image_file_name= filename )
        session.add(new_book)
        session.commit()
        return jsonify(new_book.to_dict()), 201
    
    return jsonify({'error':'Forbidden'}), 403

    
@books_bp.route("/update-book/<int:book_id>", methods= ['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = session.query(Book).filter(Book.book_id == book_id).first()
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    
    if check_admin(user):
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        if 'title' in data and data['title'].strip():
            book.title = data['title']
        if 'author' in data and data['author'].strip():
            book.author = data['author']
        if 'description' in data and data['description'].strip():
            book.description = data['description']
        if 'category' in data and data['category'].strip():
            book.category = data['category']
        if 'loan_type' in data and data['loan_type'].strip():
            book.loan_type = data['loan_type']
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(file_path)
                book.image_file_name = filename

        
        session.commit()
        return jsonify(book.to_dict()), 200
    
    return jsonify({'error':'Forbidden'}), 403


@books_bp.route("/delete-book/<int:book_id>", methods= ['DELETE'])
def delete_book(book_id):
    book = session.query(Book).filter(Book.book_id == book_id).first()
    user = check_user()
    if not user:
        return jsonify({'error':'Log in to continue'}), 401
    if check_admin(user):
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        if book.active == False:
            return jsonify({'error': 'Book allready deleted'}), 409
        if book.is_loand == True:
            return jsonify({'error' : 'Book is curently loand'}), 403
        book.active = False
        session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    
    return jsonify({'error':'Forbidden'}), 403


@books_bp.route('/search-books', methods=['GET'])
def search_books():
    title_query = request.args.get('title')
    if title_query:
        results = session.query(Book).filter(Book.title.ilike(f'%{title_query}%')).all()
        books = [book.to_dict() for book in results]
        return jsonify(books), 200
    return jsonify([]), 200