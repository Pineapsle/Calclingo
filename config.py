"""
Calcuingo Configuration
Easy-to-modify settings for the calculus learning app
"""

# Learning Topics Configuration
# To add/remove topics, simply modify this list
LEARNING_TOPICS = [
    {
        'title': 'Functions & Graphs',
        'description': 'Learn the basics of functions and how to graph them',
        'order': 1,
        'xp_reward': 10,
        'prerequisites': []
    },
    {
        'title': 'Limits',
        'description': 'Understanding limits and continuity',
        'order': 2,
        'xp_reward': 15,
        'prerequisites': [1]
    },
    {
        'title': 'Derivatives',
        'description': 'The power rule and basic differentiation',
        'order': 3,
        'xp_reward': 20,
        'prerequisites': [2]
    },
    {
        'title': 'Product & Chain Rule',
        'description': 'Advanced differentiation techniques',
        'order': 4,
        'xp_reward': 25,
        'prerequisites': [3]
    },
    {
        'title': 'Integrals',
        'description': 'Introduction to integration',
        'order': 5,
        'xp_reward': 30,
        'prerequisites': [4]
    },
    {
        'title': 'Series & Sequences',
        'description': 'Convergence and Taylor series',
        'order': 6,
        'xp_reward': 35,
        'prerequisites': [5]
    }
]

# Exercise Templates for each topic
EXERCISE_TEMPLATES = {
    1: [  # Functions & Graphs
        {
            'type': 'multiple_choice',
            'question': 'What is the domain of f(x) = √(x-2)?',
            'answer': '[2, ∞)',
            'options': ['[2, ∞)', '(-∞, 2]', '(-∞, ∞)', '[0, ∞)'],
            'hint': 'Remember: square root functions are defined when the expression inside is ≥ 0'
        },
        {
            'type': 'fill_blank',
            'question': 'If f(x) = 2x + 3, then f(5) = ___',
            'answer': '13',
            'hint': 'Substitute x = 5 into the function'
        }
    ],
    2: [  # Limits
        {
            'type': 'multiple_choice',
            'question': 'What is lim(x→2) (x² - 4)/(x - 2)?',
            'answer': '4',
            'options': ['2', '4', '0', 'undefined'],
            'hint': 'Factor the numerator and cancel common terms'
        },
        {
            'type': 'fill_blank',
            'question': 'lim(x→0) sin(x)/x = ___',
            'answer': '1',
            'hint': 'This is a fundamental limit in calculus'
        }
    ],
    3: [  # Derivatives
        {
            'type': 'multiple_choice',
            'question': 'What is the derivative of x³?',
            'answer': '3x²',
            'options': ['3x²', 'x²', '3x', 'x³'],
            'hint': 'Use the power rule: d/dx(xⁿ) = nxⁿ⁻¹'
        },
        {
            'type': 'fill_blank',
            'question': 'If f(x) = 5x², then f\'(x) = ___',
            'answer': '10x',
            'hint': 'Apply the power rule: d/dx(5x²) = 5·2x = 10x'
        }
    ],
    4: [  # Product & Chain Rule
        {
            'type': 'multiple_choice',
            'question': 'What is the derivative of (x² + 1)(x³ - 2x)?',
            'answer': '5x⁴ - 6x² - 2',
            'options': ['5x⁴ - 6x² - 2', '3x⁴ - 4x²', '2x(x³ - 2x) + (x² + 1)(3x² - 2)', '6x⁵ - 4x³'],
            'hint': 'Use the product rule: (fg)\' = f\'g + fg\''
        }
    ],
    5: [  # Integrals
        {
            'type': 'multiple_choice',
            'question': 'What is ∫(2x + 3)dx?',
            'answer': 'x² + 3x + C',
            'options': ['x² + 3x + C', '2x² + 3x + C', 'x² + 3x', '2x + 3'],
            'hint': 'Integrate term by term and don\'t forget the constant of integration'
        }
    ],
    6: [  # Series & Sequences
        {
            'type': 'multiple_choice',
            'question': 'Does the series Σ(1/n) converge?',
            'answer': 'No',
            'options': ['Yes', 'No', 'Sometimes', 'Depends on n'],
            'hint': 'This is the harmonic series, which diverges'
        }
    ]
}

# App Configuration
APP_CONFIG = {
    'app_name': 'Calcuingo',
    'app_description': 'Learn Calculus the Modern Way',
    'default_xp_per_lesson': 10,
    'max_streak_bonus': 50,
    'badges': [
        'First Steps', 'Quick Learner', 'Math Master', 
        'Calculus Champion', 'Perfect Score', 'Streak Master'
    ]
}
