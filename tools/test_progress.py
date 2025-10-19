import os
import sys

# Ensure project root is on sys.path so imports like `from app import app` work
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db
from models import User, Lesson, Exercise, Progress
from datetime import datetime

with app.app_context():
    db.create_all()
    # create user and lesson if missing
    u = User.query.filter_by(username='testuser').first()
    if not u:
        u = User(username='testuser', password='x', xp=0)
        db.session.add(u)
        db.session.commit()
    l = Lesson.query.filter_by(title='Test Lesson').first()
    if not l:
        l = Lesson(title='Test Lesson', description='desc', order=999, xp_reward=5)
        db.session.add(l)
        db.session.commit()
    # Ensure no existing progress
    p = Progress.query.filter_by(user_id=u.id, lesson_id=l.id).first()
    if p:
        db.session.delete(p)
        db.session.commit()
    # Create progress as route would
    p = Progress(user_id=u.id, lesson_id=l.id)
    db.session.add(p)
    db.session.commit()
    print('Before:', p.attempts, p.score)
    # Simulate increment
    p.attempts = (p.attempts or 0) + 1
    p.last_attempt = datetime.utcnow()
    p.score = max(float(p.score or 0.0), 1.0)
    db.session.commit()
    p2 = Progress.query.get(p.id)
    print('After:', p2.attempts, p2.score)
