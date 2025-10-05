from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            user.update_streak()
            db.session.commit()
            flash('Welcome back! 🔥', 'success')
            return redirect(url_for('learning_path'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            username=username,
            password=generate_password_hash(password),
            xp=0,
            streak=0
        )
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        flash('Welcome to Calcuingo! 🎉', 'success')
        return redirect(url_for('learning_path'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('See you later! 👋', 'info')
    return redirect(url_for('learning_path'))
