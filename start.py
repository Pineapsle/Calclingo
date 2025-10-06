#!/usr/bin/env python3
"""
Calcuingo - Simple startup script
This script properly initializes the database and starts the Flask app
"""

from app import app, db
from models import Lesson

def main():
    """Initialize database and start the app"""
    print("Starting Calcuingo...")
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if we need to create dummy data
        if Lesson.query.count() == 0:
            print("📚 Creating dummy data...")
            from dummy_data import create_dummy_data
            create_dummy_data()
        else:
            print("✅ Database already has data")
    
    print("\nStarting Flask server...")
    print("Open: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

