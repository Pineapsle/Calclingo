from models import db, Lesson, Exercise, User
import json
from config import LEARNING_TOPICS, EXERCISE_TEMPLATES

def create_dummy_data():
    """Create dummy lessons and exercises for testing using configuration"""
    
    # Create lessons from configuration
    for topic in LEARNING_TOPICS:
        lesson_data = {
            'title': topic['title'],
            'description': topic['description'],
            'order': topic['order'],
            'xp_reward': topic['xp_reward'],
            'prerequisites': json.dumps(topic['prerequisites'])
        }
        lesson = Lesson(**lesson_data)
        db.session.add(lesson)
    
    db.session.commit()
    
    # Create exercises for each lesson using templates
    for lesson_id, exercises in EXERCISE_TEMPLATES.items():
        for i, exercise_template in enumerate(exercises, 1):
            exercise_data = {
                'lesson_id': lesson_id,
                'type': exercise_template['type'],
                'question': exercise_template['question'],
                'answer': exercise_template['answer'],
                'hint': exercise_template['hint'],
                'order': i
            }
            
            # Add options for multiple choice questions
            if exercise_template['type'] == 'multiple_choice':
                exercise_data['options'] = json.dumps(exercise_template['options'])
            
            exercise = Exercise(**exercise_data)
            db.session.add(exercise)
    
    db.session.commit()
    print("✅ Dummy data created successfully from configuration!")