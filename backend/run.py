from .app import app
from flask_cors import CORS
from .routes.books import books_bp
from .routes.users import users_bp
from .routes.auth import auth_bp
from .routes.loans import loans_bp

# Enable CORS
CORS(app, origins="http://127.0.0.1:5500", supports_credentials=True)

# Register blueprints
app.register_blueprint(books_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(loans_bp)

if __name__ == "__main__":
    app.run(debug=True)
