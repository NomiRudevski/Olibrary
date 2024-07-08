# OLibrary

OLibrary is a library management system built using Flask for the backend and JavaScript with Axios for the frontend. This system allows users to manage books, users, and loans efficiently. It includes features for adding, updating, and deleting books and users, as well as managing book loans and returns.

## Features

- **Books Management**: Add, update, delete, and list books.
- **Users Management**: Add, update, delete, and list users.
- **Loans Management**: Manage book loans, including loaning books, returning books, and extending loan periods.
- **Admin Dashboard**: A dashboard for admin users to manage books, users, and loans.

## Technologies Used

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, JavaScript, Axios
- **Others**: Flask-Session, Flask-CORS

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/NomiRudevski/Olibrary.git
    cd OLibrary
    ```

2. **Create a virtual environment**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    Ensure that the `data.db` file is in the `../` directory relative to the project root.

5. **Run the application**:

    ```sh
    backend/python run.py
    ```

## Usage

### Admin Dashboard

- **Books**: Manage the library's book collection.
  - **Add New Book**: Fill out the form and click "Add new book".
  - **Update Book**: Click "Edit", update the necessary fields, and click "Update book".
  - **Delete Book**: Click "Delete" and confirm the deletion.

- **Users**: Manage user accounts.
  - **Add New User**: Fill out the form and click "Add new user".
  - **Update User**: Click "Edit", update the necessary fields, and click "Update user".
  - **Delete User**: Click "Delete" and confirm the deletion.

- **Loans**: Manage book loans.
  - **Loan a Book**: Select a book and click "Loan Book".
  - **Return a Book**: Click "Return" next to the book to mark it as returned.
  - **Extend Loan**: Click "Extend" to extend the loan period.

### Regular Users

- **View All Books**: Browse the collection of books.
- **View My Loans**: See a list of books currently on loan.

