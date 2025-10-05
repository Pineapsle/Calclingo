from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import Lesson, Exercise, Progress, User, db

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/<int:lesson_id>')
def lesson_detail(lesson_id):
    """Display a specific lesson with its exercises"""
    lesson = Lesson.query.get_or_404(lesson_id)
    exercises = Exercise.query.filter_by(lesson_id=lesson_id).order_by(Exercise.order).all()
    
    # Get user progress for this lesson
    user_progress = None
    if 'user_id' in session:
        user_progress = Progress.query.filter_by(
            user_id=session['user_id'], 
            lesson_id=lesson_id
        ).first()
    
    return render_template('lessons/lesson_detail.html', 
                         lesson=lesson, 
                         exercises=exercises,
                         user_progress=user_progress)

@lessons_bp.route('/<int:lesson_id>/exercise/<int:exercise_id>')
def exercise_detail(lesson_id, exercise_id):
    """Display a specific exercise"""
    lesson = Lesson.query.get_or_404(lesson_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    
    return render_template('lessons/exercise_detail.html', 
                         lesson=lesson, 
                         exercise=exercise)

@lessons_bp.route('/<int:lesson_id>/submit', methods=['POST'])
def submit_exercise(lesson_id):
    """Submit an exercise answer and get feedback"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    exercise_id = data.get('exercise_id')
    user_answer = data.get('answer')
    
    exercise = Exercise.query.get_or_404(exercise_id)
    user_id = session['user_id']
    
    # Check if answer is correct
    is_correct = str(user_answer).strip().lower() == str(exercise.answer).strip().lower()
    
    # Update or create progress record
    progress = Progress.query.filter_by(
        user_id=user_id, 
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = Progress(user_id=user_id, lesson_id=lesson_id)
        db.session.add(progress)
    
    progress.attempts += 1
    progress.last_attempt = db.func.now()
    
    if is_correct:
        progress.score = max(progress.score, 1.0)  # Full points for correct answer
        progress.completed = True
        
        # Award XP to user
        user = User.query.get(user_id)
        user.xp += lesson.xp_reward
        db.session.commit()
        
        return jsonify({
            'correct': True,
            'message': 'Great job! 🎉',
            'xp_earned': lesson.xp_reward,
            'total_xp': user.xp
        })
    else:
        return jsonify({
            'correct': False,
            'message': f'Not quite right. Hint: {exercise.hint or "Try again!"}',
            'hint': exercise.hint
        })
