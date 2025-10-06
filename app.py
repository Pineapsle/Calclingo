from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

# Initialize Flask application
app = Flask(__name__)

# Configuration settings
# TODO: Move to environment variables for production security
app.config['SECRET_KEY'] = 'calcuingo-secret-key-2024'  # Used for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calcuingo.db'  # SQLite database file location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system

# Import database models first (required before db initialization)
from models import db, User, Lesson, Exercise, Progress

# Initialize SQLAlchemy database with Flask app
db.init_app(app)

# Import route blueprints (modular route organization)
from routes.auth import auth_bp      # Authentication routes (login, register, logout)
from routes.lessons import lessons_bp  # Lesson-related routes (view lessons, exercises)
from routes.progress import progress_bp  # User progress tracking routes

# Register route blueprints with URL prefixes
app.register_blueprint(auth_bp, url_prefix='/auth')      # Routes: /auth/login, /auth/register, etc.
app.register_blueprint(lessons_bp, url_prefix='/lessons')  # Routes: /lessons/1, /lessons/1/exercises, etc.
app.register_blueprint(progress_bp, url_prefix='/progress')  # Routes: /progress/save, /progress/update, etc.

@app.route('/')
def index():
    """Home page - redirects to learning path"""
    return redirect(url_for('learning_path'))

@app.route('/learning-path')
def learning_path():
    """
    Main learning path page with Duolingo-style nodes
    Displays all lessons in order and user progress if logged in
    """
    # Get all lessons ordered by their sequence
    lessons = Lesson.query.order_by(Lesson.order).all()
    
    # Get user progress if logged in (for showing completion status)
    user_progress = {}
    if 'user_id' in session:
        user_id = session['user_id']
        progress_records = Progress.query.filter_by(user_id=user_id).all()
        # Create a dictionary mapping lesson_id to progress record for easy lookup
        user_progress = {p.lesson_id: p for p in progress_records}
    
    return render_template('learning_path.html', lessons=lessons, user_progress=user_progress)

@app.route('/profile')
def profile():
    """
    User profile page showing XP, streak, badges, and learning statistics
    Requires user to be logged in
    """
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get user from database
    user = User.query.get(session['user_id'])
    if not user:
        # User doesn't exist (session invalid), redirect to login
        return redirect(url_for('auth.login'))
    
    # Calculate user's learning statistics
    completed_lessons = Progress.query.filter_by(user_id=user.id, completed=True).count()
    total_lessons = Lesson.query.count()
    
    return render_template('profile.html', 
                         user=user, 
                         completed_lessons=completed_lessons,
                         total_lessons=total_lessons)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create dummy data if no lessons exist
        if Lesson.query.count() == 0:
            from dummy_data import create_dummy_data
            create_dummy_data()
    
    app.run(debug=True)

