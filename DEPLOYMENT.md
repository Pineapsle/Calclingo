# Calcuingo Deployment Guide

## Production Deployment

### Prerequisites
- Python 3.8+
- PostgreSQL (for production) or SQLite (for development)
- Nginx (recommended for production)
- SSL certificate (for HTTPS)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Calclingo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp env.example .env
   # Edit .env with your production values
   ```

### Database Setup

#### For Development (SQLite)
```bash
python run.py
```

#### For Production (PostgreSQL)
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE calcuingo;
   CREATE USER calcuingo_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE calcuingo TO calcuingo_user;
   ```
3. Update `.env`:
   ```
   DATABASE_URL=postgresql://calcuingo_user:secure_password@localhost:5432/calcuingo
   ```

### Production Server Setup

#### Using Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

#### Using Nginx (Recommended)
1. Install Nginx
2. Create configuration file `/etc/nginx/sites-available/calcuingo`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       # Static files
       location /static {
           alias /path/to/Calclingo/static;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```
3. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/calcuingo /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### SSL/HTTPS Setup

1. **Using Let's Encrypt (Free)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. **Update environment variables**
   ```
   SESSION_COOKIE_SECURE=True
   ```

### Security Considerations

1. **Environment Variables**
   - Never commit `.env` file
   - Use strong, unique SECRET_KEY
   - Use environment-specific database URLs

2. **Database Security**
   - Use strong database passwords
   - Limit database user permissions
   - Enable SSL for database connections

3. **Application Security**
   - Keep dependencies updated
   - Use HTTPS in production
   - Implement rate limiting (consider Flask-Limiter)
   - Regular security audits

### Monitoring and Logging

1. **Application Logs**
   ```bash
   # Using systemd service
   sudo journalctl -u calcuingo -f
   ```

2. **Database Monitoring**
   - Monitor database performance
   - Set up database backups
   - Monitor disk space

### Backup Strategy

1. **Database Backups**
   ```bash
   # PostgreSQL backup
   pg_dump calcuingo > backup_$(date +%Y%m%d).sql
   
   # SQLite backup
   cp calcuingo.db backup_$(date +%Y%m%d).db
   ```

2. **Application Backups**
   - Backup application code
   - Backup static files
   - Backup configuration files

### Performance Optimization

1. **Database Optimization**
   - Add database indexes for frequently queried fields
   - Use connection pooling
   - Monitor query performance

2. **Application Optimization**
   - Use Redis for session storage (optional)
   - Implement caching for static content
   - Use CDN for static assets

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Health Checks

Add health check endpoint:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Scaling Considerations

1. **Horizontal Scaling**
   - Use load balancer (Nginx, HAProxy)
   - Session storage in Redis
   - Database read replicas

2. **Vertical Scaling**
   - Increase server resources
   - Optimize database queries
   - Use caching strategies

### Maintenance

1. **Regular Updates**
   - Update dependencies monthly
   - Security patches immediately
   - Monitor for vulnerabilities

2. **Database Maintenance**
   - Regular backups
   - Index optimization
   - Query performance monitoring

### Troubleshooting

1. **Common Issues**
   - Database connection errors
   - Static file serving issues
   - SSL certificate problems

2. **Debug Mode**
   - Only enable in development
   - Never use in production
   - Use proper logging instead
