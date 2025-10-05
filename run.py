#!/usr/bin/env python3
"""
Calcuingo - Duolingo-style Calculus Learning App
Startup script to run the Flask application
"""

import os
import sys
from app import app, db

def main():
    """Main function to start the Calcuingo app"""
    print("🧮 Starting Calcuingo - Duolingo-style Calculus Learning App")
    print("=" * 60)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
        
        # Create dummy data if no lessons exist
        from models import Lesson
        if Lesson.query.count() == 0:
            from dummy_data import create_dummy_data
            create_dummy_data()
            print("✅ Dummy data created")
        else:
            print("✅ Database already has data")
    
    print("\n🚀 Starting Flask development server...")
    print("📍 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
