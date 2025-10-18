from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import Lesson, Exercise, Progress, User, db
from datetime import datetime

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
        flash('Please log in to submit answers', 'error')
        return redirect(url_for('auth.login'))
    
    exercise_id = request.form.get('exercise_id')
    user_answer = request.form.get('answer')
    
    if not exercise_id or not user_answer:
        flash('Please provide an answer', 'error')
        return redirect(url_for('lessons.lesson_detail', lesson_id=lesson_id)) # Might need to change this cause we getting an error when we submit an answer. Redirect error. CD out and then into the current directory
    
    exercise = Exercise.query.get_or_404(exercise_id)
    lesson = Lesson.query.get_or_404(lesson_id)
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
    progress.last_attempt = datetime.utcnow()
    
    if is_correct:
        progress.score = max(progress.score, 1.0)  # Full points for correct answer
        progress.completed = True
        
        # Award XP to user
        user = User.query.get(user_id)
        user.xp += lesson.xp_reward
        db.session.commit()
        
        flash(f'Great job! 🎉 You earned {lesson.xp_reward} XP!', 'success')
    else:
        # Commit the attempt even for wrong answers
        db.session.commit()
        flash(f'Not quite right. {exercise.hint or "Try again!"}', 'warning')
    
    return redirect(url_for('lessons.lesson_detail', lesson_id=lesson_id))
