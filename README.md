# 🧮 Calcuingo - Duolingo-style Calculus Learning App

A gamified web application for learning calculus step by step, inspired by Duolingo's engaging learning experience.

## ✨ Features

- **🎯 Duolingo-style Learning Path**: Visual progression through calculus topics
- **📚 Multiple Exercise Types**: Multiple choice, fill-in-the-blank, drag-and-drop
- **🏆 Gamification**: XP points, streaks, badges, and achievements
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🎨 Beautiful UI**: Colorful, animated interface with "Calcy the Parrot" mascot
- **🔐 User Authentication**: Login/register system with progress tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Calcuingo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python start.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Learning Path

The app includes a structured learning path with these calculus topics:

1. **Functions & Graphs** - Basic function concepts and graphing
2. **Limits** - Understanding limits and continuity  
3. **Derivatives** - Power rule and basic differentiation
4. **Product & Chain Rule** - Advanced differentiation techniques
5. **Integrals** - Introduction to integration
6. **Series & Sequences** - Convergence and Taylor series

## 🎮 Exercise Types

- **Multiple Choice**: Select the correct answer from options
- **Fill-in-the-Blank**: Type your answer directly
- **Drag & Drop**: Match functions with their derivatives (coming soon)
- **Interactive Graphs**: Plot functions and visualize concepts (coming soon)

## 🏗️ Project Structure

```
Calcuingo/
├── app.py                 # Flask application entry point
├── models.py              # Database models (User, Lesson, Exercise, Progress)
├── dummy_data.py          # Sample data for testing
├── requirements.txt       # Python dependencies
├── routes/                # Blueprint modules
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   ├── lessons.py        # Lesson and exercise routes
│   └── progress.py       # Progress tracking routes
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template
│   ├── learning_path.html # Main learning path page
│   ├── profile.html      # User profile page
│   ├── auth/            # Authentication templates
│   └── lessons/         # Lesson templates
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Custom styling
    └── js/
        └── main.js      # JavaScript functionality
```

## 🎨 Design Features

- **Duolingo-inspired UI**: Bright colors, rounded corners, smooth animations
- **Responsive Grid**: Adapts to different screen sizes
- **Interactive Elements**: Hover effects, click animations, progress indicators
- **Mascot Character**: "Calcy the Parrot" provides encouragement and hints
- **Gamification**: XP bars, streak counters, achievement badges

## 🔧 Development

### Adding New Lessons

1. Add lesson data to `dummy_data.py`
2. Create exercises for the lesson
3. Update the learning path template if needed

### Adding New Exercise Types

1. Add the exercise type to the `Exercise` model
2. Create a template for the exercise type
3. Add JavaScript handling for the exercise type
4. Update the lesson detail template

### Customizing the UI

- Modify `static/css/style.css` for styling changes
- Update `static/js/main.js` for JavaScript functionality
- Edit templates in the `templates/` directory

## 🚀 Deployment

The app is ready for deployment on platforms like:
- **Heroku**: Add a `Procfile` and configure environment variables
- **Render**: Connect your GitHub repository
- **AWS**: Use Elastic Beanstalk or EC2
- **DigitalOcean**: Deploy as a Python app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- [ ] Interactive graph exercises with Plotly.js
- [ ] Advanced drag-and-drop matching
- [ ] Social features (leaderboards, friends)
- [ ] Mobile app version
- [ ] Advanced analytics and progress tracking
- [ ] More calculus topics (multivariable, differential equations)

---

**Happy Learning! 🧮✨**

*Made with ❤️ for calculus lovers*
