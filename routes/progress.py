from flask import Blueprint, jsonify, session
from models import Progress, User, db

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/user-stats')
def user_stats():
    """Get current user's progress statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get progress statistics
    completed_lessons = Progress.query.filter_by(user_id=user_id, completed=True).count()
    total_attempts = db.session.query(db.func.sum(Progress.attempts)).filter_by(user_id=user_id).scalar() or 0
    
    return jsonify({
        'xp': user.xp,
        'streak': user.streak,
        'badges': user.get_badges(),
        'completed_lessons': completed_lessons,
        'total_attempts': total_attempts
    })

@progress_bp.route('/update-lesson-status/<int:lesson_id>', methods=['POST'])
def update_lesson_status(lesson_id):
    """Update lesson completion status"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = session['user_id']
    
    # Get or create progress record
    progress = Progress.query.filter_by(
        user_id=user_id, 
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = Progress(user_id=user_id, lesson_id=lesson_id)
        db.session.add(progress)
    
    progress.completed = True
    progress.score = 1.0
    
    # Award XP
    from models import Lesson
    lesson = Lesson.query.get(lesson_id)
    user = User.query.get(user_id)
    user.xp += lesson.xp_reward
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'xp_earned': lesson.xp_reward,
        'total_xp': user.xp
    })
