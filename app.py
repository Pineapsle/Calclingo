from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'calcuingo-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calcuingo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models first
from models import db, User, Lesson, Exercise, Progress

# Initialize db with app
db.init_app(app)

# Import routes
from routes.auth import auth_bp
from routes.lessons import lessons_bp
from routes.progress import progress_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(lessons_bp, url_prefix='/lessons')
app.register_blueprint(progress_bp, url_prefix='/progress')

@app.route('/')
def index():
    """Home page - redirects to learning path"""
    return redirect(url_for('learning_path'))

@app.route('/learning-path')
def learning_path():
    """Main learning path page with Duolingo-style nodes"""
    lessons = Lesson.query.order_by(Lesson.order).all()
    
    # Get user progress if logged in
    user_progress = {}
    if 'user_id' in session:
        user_id = session['user_id']
        progress_records = Progress.query.filter_by(user_id=user_id).all()
        user_progress = {p.lesson_id: p for p in progress_records}
    
    return render_template('learning_path.html', lessons=lessons, user_progress=user_progress)

@app.route('/profile')
def profile():
    """User profile page showing XP, streak, badges"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('auth.login'))
    
    # Get user's completed lessons
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

