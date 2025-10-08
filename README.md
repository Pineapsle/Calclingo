# Calcuingo - Modern Calculus Learning App

A clean, modern web application for learning calculus with a focus on simplicity and modularity.

## Features

- **6 Core Topics**: Functions & Graphs, Limits, Derivatives, Product & Chain Rule, Integrals, Series & Sequences
- **User Authentication**: Simple login/logout system
- **Progress Tracking**: XP system and completion tracking
- **No JavaScript**: Pure server-side rendering for simplicity
- **Modular Design**: Easy to add/remove topics
- **Modern UI**: Clean, responsive design

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python start.py
   ```

3. Open your browser to `http://localhost:5000`

## Adding/Removing Topics

The application is designed to be easily modifiable. To add or remove topics:

1. **Edit `config.py`**: Modify the `LEARNING_TOPICS` list to add/remove topics
2. **Add Exercises**: Update the `EXERCISE_TEMPLATES` dictionary with exercises for new topics
3. **Restart the app**: The changes will be applied on the next startup

### Example: Adding a New Topic

```python
# In config.py, add to LEARNING_TOPICS:
{
    'title': 'Advanced Integration',
    'description': 'Integration by parts and substitution',
    'order': 7,
    'xp_reward': 40,
    'prerequisites': [6]
}

# Add exercises to EXERCISE_TEMPLATES:
7: [
    {
        'type': 'multiple_choice',
        'question': 'What is ∫x·e^x dx?',
        'answer': 'x·e^x - e^x + C',
        'options': ['x·e^x - e^x + C', 'x·e^x + C', 'e^x + C', 'x·e^x'],
        'hint': 'Use integration by parts: ∫u dv = uv - ∫v du'
    }
]
```

## Project Structure

```
Calcuingo/
├── app.py              # Main Flask application
├── models.py           # Database models
├── config.py           # Configuration (topics, exercises)
├── dummy_data.py       # Data initialization
├── start.py            # Application starter
├── routes/             # Route modules
│   ├── auth.py         # Authentication routes
│   ├── lessons.py     # Lesson routes
│   └── progress.py     # Progress tracking
├── templates/          # HTML templates
├── static/css/         # Stylesheets
└── instance/           # Database files
```

## Key Design Decisions

- **No JavaScript**: Everything works with server-side rendering for simplicity
- **Modular Topics**: Easy to modify the curriculum by editing `config.py`
- **Clean UI**: Modern, responsive design without complex animations
- **Simple Authentication**: Basic login/logout without complex features
- **Progress Tracking**: XP and completion system for motivation

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5 + Custom CSS
- **Authentication**: Flask sessions
- **Styling**: Modern CSS with CSS variables

## Development

To modify the application:

1. **Topics**: Edit `config.py` → `LEARNING_TOPICS`
2. **Exercises**: Edit `config.py` → `EXERCISE_TEMPLATES`
3. **Styling**: Edit `static/css/style.css`
4. **Routes**: Modify files in `routes/` directory
5. **Templates**: Update HTML files in `templates/`

The application is designed to be simple, maintainable, and easy to extend.