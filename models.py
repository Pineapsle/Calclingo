from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

# Initialize SQLAlchemy database instance
db = SQLAlchemy()

class User(db.Model):
    """
    User model representing learners in the system
    Stores authentication info, progress tracking, and gamification data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username for login
    password = db.Column(db.String(120), nullable=False)  # Hashed password (not plain text)
    xp = db.Column(db.Integer, default=0)  # Experience points earned from completing lessons
    streak = db.Column(db.Integer, default=0)  # Daily login streak counter
    last_login = db.Column(db.DateTime, default=datetime.utcnow)  # Track last login for streak calculation
    badges = db.Column(db.Text, default='[]')  # JSON string storing earned badge names
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_badges(self):
        """Convert JSON string badges to Python list"""
        try:
            return json.loads(self.badges)
        except:
            return []  # Return empty list if JSON is invalid
    
    def add_badge(self, badge_name):
        """Add a new badge to user's collection (prevents duplicates)"""
        badges = self.get_badges()
        if badge_name not in badges:
            badges.append(badge_name)
            self.badges = json.dumps(badges)
    
    def update_streak(self):
        """
        Update daily login streak based on last login date
        - Increments streak if logged in yesterday
        - Resets to 1 if gap is more than 1 day
        - Sets to 1 if first login
        """
        now = datetime.utcnow()
        if self.last_login:
            days_diff = (now - self.last_login).days
            if days_diff == 1:
                self.streak += 1  # Perfect streak continuation
            elif days_diff > 1:
                self.streak = 1   # Streak broken, start over
        else:
            self.streak = 1       # First login
        
        self.last_login = now

class Lesson(db.Model):
    """
    Lesson model representing individual calculus lessons
    Each lesson has exercises and can have prerequisites
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Lesson title (e.g., "Introduction to Limits")
    description = db.Column(db.Text)  # Detailed lesson description
    status = db.Column(db.String(20), default='locked')  # locked, in-progress, completed
    order = db.Column(db.Integer, nullable=False)  # Display order in learning path
    xp_reward = db.Column(db.Integer, default=10)  # XP points awarded for completion
    prerequisites = db.Column(db.Text)  # JSON string of prerequisite lesson IDs
    
    def __repr__(self):
        return f'<Lesson {self.title}>'
    
    def get_prerequisites(self):
        """Convert JSON string prerequisites to Python list"""
        try:
            return json.loads(self.prerequisites) if self.prerequisites else []
        except:
            return []  # Return empty list if JSON is invalid

class Exercise(db.Model):
    """
    Exercise model representing individual questions within lessons
    Supports different question types: multiple choice, fill-in-blank, etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)  # Parent lesson
    type = db.Column(db.String(50), nullable=False)  # multiple_choice, fill_blank, drag_drop, graph
    question = db.Column(db.Text, nullable=False)  # The exercise question/prompt
    answer = db.Column(db.Text, nullable=False)  # Correct answer (can be complex for math problems)
    options = db.Column(db.Text)  # JSON string for multiple choice options
    hint = db.Column(db.Text)  # Optional hint for students
    order = db.Column(db.Integer, default=0)  # Order within the lesson
    
    def __repr__(self):
        return f'<Exercise {self.id}>'
    
    def get_options(self):
        """Get options as a list"""
        try:
            return json.loads(self.options) if self.options else []
        except:
            return []

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float, default=0.0)
    attempts = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Progress {self.user_id}-{self.lesson_id}>'

