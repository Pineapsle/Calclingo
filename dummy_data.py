from models import db, Lesson, Exercise, User
import json

def create_dummy_data():
    """Create dummy lessons and exercises for testing"""
    
    # Create lessons
    lessons_data = [
        {
            'title': 'Functions & Graphs',
            'description': 'Learn the basics of functions and how to graph them',
            'order': 1,
            'xp_reward': 10,
            'prerequisites': '[]'
        },
        {
            'title': 'Limits',
            'description': 'Understanding limits and continuity',
            'order': 2,
            'xp_reward': 15,
            'prerequisites': '[1]'
        },
        {
            'title': 'Derivatives',
            'description': 'The power rule and basic differentiation',
            'order': 3,
            'xp_reward': 20,
            'prerequisites': '[2]'
        },
        {
            'title': 'Product & Chain Rule',
            'description': 'Advanced differentiation techniques',
            'order': 4,
            'xp_reward': 25,
            'prerequisites': '[3]'
        },
        {
            'title': 'Integrals',
            'description': 'Introduction to integration',
            'order': 5,
            'xp_reward': 30,
            'prerequisites': '[4]'
        },
        {
            'title': 'Series & Sequences',
            'description': 'Convergence and Taylor series',
            'order': 6,
            'xp_reward': 35,
            'prerequisites': '[5]'
        }
    ]
    
    for lesson_data in lessons_data:
        lesson = Lesson(**lesson_data)
        db.session.add(lesson)
    
    db.session.commit()
    
    # Create exercises for each lesson
    exercises_data = [
        # Lesson 1: Functions & Graphs
        {
            'lesson_id': 1,
            'type': 'multiple_choice',
            'question': 'What is the domain of f(x) = √(x-2)?',
            'answer': '[2, ∞)',
            'options': '["[2, ∞)", "(-∞, 2]", "(-∞, ∞)", "[0, ∞)"]',
            'hint': 'Remember: square root functions are defined when the expression inside is ≥ 0',
            'order': 1
        },
        {
            'lesson_id': 1,
            'type': 'fill_blank',
            'question': 'If f(x) = 2x + 3, then f(5) = ___',
            'answer': '13',
            'hint': 'Substitute x = 5 into the function',
            'order': 2
        },
        
        # Lesson 2: Limits
        {
            'lesson_id': 2,
            'type': 'multiple_choice',
            'question': 'What is lim(x→2) (x² - 4)/(x - 2)?',
            'answer': '4',
            'options': '["2", "4", "0", "undefined"]',
            'hint': 'Factor the numerator and cancel common terms',
            'order': 1
        },
        {
            'lesson_id': 2,
            'type': 'fill_blank',
            'question': 'lim(x→0) sin(x)/x = ___',
            'answer': '1',
            'hint': 'This is a fundamental limit in calculus',
            'order': 2
        },
        
        # Lesson 3: Derivatives
        {
            'lesson_id': 3,
            'type': 'multiple_choice',
            'question': 'What is the derivative of x³?',
            'answer': '3x²',
            'options': '["3x²", "x²", "3x", "x³"]',
            'hint': 'Use the power rule: d/dx(xⁿ) = nxⁿ⁻¹',
            'order': 1
        },
        {
            'lesson_id': 3,
            'type': 'fill_blank',
            'question': 'If f(x) = 5x², then f\'(x) = ___',
            'answer': '10x',
            'hint': 'Apply the power rule: d/dx(5x²) = 5·2x = 10x',
            'order': 2
        },
        
        # Lesson 4: Product & Chain Rule
        {
            'lesson_id': 4,
            'type': 'multiple_choice',
            'question': 'What is the derivative of (x² + 1)(x³ - 2x)?',
            'answer': '5x⁴ - 6x² - 2',
            'options': '["5x⁴ - 6x² - 2", "3x⁴ - 4x²", "2x(x³ - 2x) + (x² + 1)(3x² - 2)", "6x⁵ - 4x³"]',
            'hint': 'Use the product rule: (fg)\' = f\'g + fg\'',
            'order': 1
        },
        
        # Lesson 5: Integrals
        {
            'lesson_id': 5,
            'type': 'multiple_choice',
            'question': 'What is ∫(2x + 3)dx?',
            'answer': 'x² + 3x + C',
            'options': '["x² + 3x + C", "2x² + 3x + C", "x² + 3x", "2x + 3"]',
            'hint': 'Integrate term by term and don\'t forget the constant of integration',
            'order': 1
        },
        
        # Lesson 6: Series & Sequences
        {
            'lesson_id': 6,
            'type': 'multiple_choice',
            'question': 'Does the series Σ(1/n) converge?',
            'answer': 'No',
            'options': '["Yes", "No", "Sometimes", "Depends on n"]',
            'hint': 'This is the harmonic series, which diverges',
            'order': 1
        }
    ]
    
    for exercise_data in exercises_data:
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
    
    db.session.commit()
    print("✅ Dummy data created successfully!")
