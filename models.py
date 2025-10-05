from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    xp = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    badges = db.Column(db.Text, default='[]')  # JSON string of badge names
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_badges(self):
        """Get badges as a list"""
        try:
            return json.loads(self.badges)
        except:
            return []
    
    def add_badge(self, badge_name):
        """Add a new badge"""
        badges = self.get_badges()
        if badge_name not in badges:
            badges.append(badge_name)
            self.badges = json.dumps(badges)
    
    def update_streak(self):
        """Update streak based on last login"""
        now = datetime.utcnow()
        if self.last_login:
            days_diff = (now - self.last_login).days
            if days_diff == 1:
                self.streak += 1
            elif days_diff > 1:
                self.streak = 1
        else:
            self.streak = 1
        
        self.last_login = now

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='locked')  # locked, in-progress, completed
    order = db.Column(db.Integer, nullable=False)
    xp_reward = db.Column(db.Integer, default=10)
    prerequisites = db.Column(db.Text)  # JSON string of lesson IDs
    
    def __repr__(self):
        return f'<Lesson {self.title}>'
    
    def get_prerequisites(self):
        """Get prerequisites as a list"""
        try:
            return json.loads(self.prerequisites) if self.prerequisites else []
        except:
            return []

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # multiple_choice, fill_blank, drag_drop, graph
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)  # JSON string for multiple choice options
    hint = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    
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

