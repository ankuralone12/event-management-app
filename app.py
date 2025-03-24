import os
from flask import Flask, redirect, url_for
from models.models import db, User
from flask_login import LoginManager
from auth.auth import auth_bp
from controllers.event_controller import event_bp

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = os.urandom(24)

# Database configuration
DATABASE_FOLDER = os.path.join(os.getcwd(), "database")
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "events.db")

if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_FILE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# ✅ Create and configure login manager properly
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# ✅ User loader for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(event_bp, url_prefix='/events')

# Home route
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# Create DB tables
with app.app_context():
    db.create_all()

# Run app
if __name__ == '__main__':
    app.run()
