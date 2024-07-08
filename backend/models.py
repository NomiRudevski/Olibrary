from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os

Base = declarative_base()
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'images')

#########################################################################################################

class Book(Base):
    __tablename__ = "books"

    book_id = Column("book_id", Integer, primary_key=True, autoincrement= True)
    active = Column("active", BOOLEAN)
    title = Column("title", String)
    author = Column("author", String)
    description = Column("description", String)
    category = Column("category", String)
    is_loand = Column("is_loand", BOOLEAN)
    loan_type = Column("loan_type", Integer)
    image_file_name = Column("Image_file_name", String)

    loans = relationship("Loan", back_populates="book")


    def __init__(self, title, author, description, category, loan_type, image_file_name, active = True, is_loaned = False):
        self.title = title
        self.author = author
        self.description = description
        self.category = category
        self.loan_type = loan_type
        self.active = active
        self.is_loand = is_loaned
        self.image_file_name = image_file_name

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'category': self.category,
            'loan_type' : self.loan_type,
            'is_loaned': self.is_loand,
            'image_file_name' : self.image_file_name
        }
    
#########################################################################################################

class User(Base):
    __tablename__ = "users"

    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    active = Column("active", BOOLEAN)
    user_name = Column("user_name", String)
    user_email = Column("user_email", String)
    user_password = Column("user_password", String)
    permission_level = Column("permission_level", CHAR)

    loans = relationship("Loan", back_populates="user")


    def __init__(self, user_name, user_email, user_password, active= True, permission_level='U'):
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.permission_level = permission_level
        self.active = active

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'premission_level' :self.permission_level
        }

#########################################################################################################

class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column("loan_id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"))
    book_id = Column("book_id", Integer, ForeignKey("books.book_id"))
    loan_date = Column("loan_date", String)
    return_date = Column("return_date", String)
    is_late = Column("is_late", BOOLEAN)
    active = Column("active", BOOLEAN)

    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")

    def __init__(self, user_id, book_id, loan_date, return_date, is_late= False, active=True):
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_late = is_late
        self.active = active

    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'user_name': self.user.user_name,
            'book_title': self.book.title,
            'loan_date': self.loan_date,
            'return_date': self.return_date,
            'is_late': self.is_late,
            'active': self.active
        }