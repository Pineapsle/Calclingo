# Calcuingo Database Architecture

## Overview

Calcuingo uses a relational database design optimized for a Duolingo-style calculus learning application. The database supports user management, lesson progression, exercise tracking, and gamification features.

## Database Schema

### Core Tables

#### 1. User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    xp INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
    badges TEXT DEFAULT '[]'
);
```

**Purpose**: Stores user accounts and gamification data
**Key Features**:
- Secure password hashing (Werkzeug)
- Experience points (XP) tracking
- Daily streak calculation
- JSON-based badge system

#### 2. Lesson Table
```sql
CREATE TABLE lesson (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'locked',
    order INTEGER NOT NULL,
    xp_reward INTEGER DEFAULT 10,
    prerequisites TEXT
);
```

**Purpose**: Defines learning modules in sequence
**Key Features**:
- Ordered learning path
- Prerequisite system (JSON-based)
- XP rewards per lesson
- Status tracking (locked/in-progress/completed)

#### 3. Exercise Table
```sql
CREATE TABLE exercise (
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    options TEXT,
    hint TEXT,
    order INTEGER DEFAULT 0,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id)
);
```

**Purpose**: Individual questions within lessons
**Key Features**:
- Multiple question types (multiple_choice, fill_blank, etc.)
- JSON-based options for multiple choice
- Hint system
- Ordered within lessons

#### 4. Progress Table
```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    lesson_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    score FLOAT DEFAULT 0.0,
    attempts INTEGER DEFAULT 0,
    last_attempt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (lesson_id) REFERENCES lesson(id)
);
```

**Purpose**: Tracks user progress through lessons
**Key Features**:
- Completion tracking
- Score calculation
- Attempt counting
- Timestamp tracking

## Database Relationships

### Entity Relationship Diagram
```
User (1) ----< Progress (N) >---- (1) Lesson
Lesson (1) ----< Exercise (N)
```

### Key Relationships:
1. **User → Progress**: One-to-many (user can have multiple progress records)
2. **Lesson → Progress**: One-to-many (lesson can have multiple user progress records)
3. **Lesson → Exercise**: One-to-many (lesson contains multiple exercises)

## Data Flow

### User Registration Flow
1. User submits registration form
2. Password is hashed using Werkzeug
3. User record created with default values
4. Session established

### Lesson Progression Flow
1. User accesses lesson
2. System checks prerequisites
3. If prerequisites met, lesson unlocked
4. User completes exercises
5. Progress updated
6. XP awarded
7. Next lesson unlocked

### Exercise Submission Flow
1. User submits answer
2. System validates answer
3. Progress record updated
4. If correct: XP awarded, lesson marked complete
5. If incorrect: Hint shown, attempt counted

## Database Design Patterns

### 1. JSON Fields for Flexibility
- **Prerequisites**: Stored as JSON array of lesson IDs
- **Badges**: Stored as JSON array of badge names
- **Options**: Stored as JSON array for multiple choice options

### 2. Gamification Data
- **XP System**: Cumulative experience points
- **Streak System**: Daily login tracking
- **Badge System**: Achievement tracking
- **Progress Tracking**: Completion percentages

### 3. Learning Path Design
- **Sequential Ordering**: Lessons have order field
- **Prerequisite System**: JSON-based dependency tracking
- **Status Management**: Locked/In-progress/Completed states

## Production Considerations

### 1. Database Choice

#### Development: SQLite
- **Pros**: Zero configuration, file-based, perfect for development
- **Cons**: Limited concurrency, no network access
- **Use Case**: Local development, testing

#### Production: PostgreSQL
- **Pros**: High performance, ACID compliance, advanced features
- **Cons**: Requires setup and maintenance
- **Use Case**: Production deployments, high-traffic applications

### 2. Performance Optimization

#### Indexing Strategy
```sql
-- User lookups
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_user_last_login ON user(last_login);

-- Progress tracking
CREATE INDEX idx_progress_user_lesson ON progress(user_id, lesson_id);
CREATE INDEX idx_progress_completed ON progress(completed);

-- Lesson ordering
CREATE INDEX idx_lesson_order ON lesson(order);

-- Exercise ordering
CREATE INDEX idx_exercise_lesson_order ON exercise(lesson_id, order);
```

#### Query Optimization
- Use `select_related()` for foreign key joins
- Implement pagination for large datasets
- Cache frequently accessed data
- Use database connection pooling

### 3. Data Integrity

#### Constraints
```sql
-- Ensure positive XP values
ALTER TABLE user ADD CONSTRAINT check_xp_positive CHECK (xp >= 0);

-- Ensure valid lesson order
ALTER TABLE lesson ADD CONSTRAINT check_order_positive CHECK (order > 0);

-- Ensure valid progress score
ALTER TABLE progress ADD CONSTRAINT check_score_range CHECK (score >= 0.0 AND score <= 1.0);
```

#### Validation
- Application-level validation for all inputs
- Database-level constraints for critical data
- Regular data integrity checks

### 4. Backup Strategy

#### Automated Backups
```bash
# PostgreSQL backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump calcuingo > backup_$DATE.sql
gzip backup_$DATE.sql
```

#### Backup Retention
- Daily backups for 30 days
- Weekly backups for 12 weeks
- Monthly backups for 12 months

### 5. Security Considerations

#### Data Protection
- Password hashing (Werkzeug PBKDF2)
- SQL injection prevention (SQLAlchemy ORM)
- Input validation and sanitization
- HTTPS for data transmission

#### Access Control
- Database user with minimal privileges
- Connection encryption
- Regular security audits
- Principle of least privilege

### 6. Scalability Planning

#### Horizontal Scaling
- Read replicas for query distribution
- Database sharding by user ID
- Caching layer (Redis)
- Load balancing

#### Vertical Scaling
- Increased server resources
- Database optimization
- Query performance tuning
- Connection pooling

## Migration Strategy

### 1. Schema Evolution
- Version-controlled migrations
- Backward compatibility
- Data transformation scripts
- Rollback procedures

### 2. Data Migration
```python
# Example migration script
def migrate_user_badges():
    """Convert old badge format to new JSON format"""
    users = User.query.all()
    for user in users:
        if isinstance(user.badges, str) and not user.badges.startswith('['):
            # Convert old format to JSON
            user.badges = json.dumps([user.badges])
    db.session.commit()
```

## Monitoring and Analytics

### 1. Performance Metrics
- Query execution times
- Database connection usage
- Index utilization
- Lock contention

### 2. Business Metrics
- User engagement (daily active users)
- Learning progress (completion rates)
- Exercise difficulty (success rates)
- Feature usage (popular lessons)

### 3. Health Checks
```python
@app.route('/health/database')
def database_health():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

## Future Enhancements

### 1. Advanced Features
- Adaptive learning algorithms
- Personalized lesson recommendations
- Social features (leaderboards, sharing)
- Offline learning support

### 2. Data Analytics
- Learning pattern analysis
- Difficulty adjustment algorithms
- Performance prediction models
- A/B testing framework

### 3. Integration Capabilities
- Third-party authentication (OAuth)
- Learning management system integration
- API for mobile applications
- Webhook support for external services

## Conclusion

The Calcuingo database architecture is designed for:
- **Scalability**: Handles growing user base and content
- **Performance**: Optimized queries and indexing
- **Flexibility**: JSON fields allow easy feature additions
- **Security**: Proper data protection and access control
- **Maintainability**: Clear structure and documentation

This architecture supports the core learning functionality while providing a foundation for future enhancements and scaling requirements.
