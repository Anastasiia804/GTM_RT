# Production Deployment Guide

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+
- Node.js 18+
- Nginx
- Domain configured (tsprtg.com)
- SSL certificate (Let's Encrypt recommended)

## Installation Steps

### 1. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/Anastasiia804/GTM_RT.git tsprtg
cd tsprtg
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production settings
```

### 3. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 4. Configure Database

The SQLite database will be created automatically on first run. For production, consider using PostgreSQL:

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE tsprtg;
CREATE USER tsprtg WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE tsprtg TO tsprtg;
\q

# Update .env
DATABASE_URL=postgresql://tsprtg:your-password@localhost/tsprtg
```

### 5. Configure Systemd Service

```bash
# Copy service file
sudo cp deployment/tsprtg-backend.service /etc/systemd/system/

# Edit paths if needed
sudo nano /etc/systemd/system/tsprtg-backend.service

# Enable and start service
sudo systemctl enable tsprtg-backend
sudo systemctl start tsprtg-backend
sudo systemctl status tsprtg-backend
```

### 6. Configure Nginx

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/tsprtg.com

# Update with your domain and SSL paths
sudo nano /etc/nginx/sites-available/tsprtg.com

# Enable site
sudo ln -s /etc/nginx/sites-available/tsprtg.com /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 7. Setup SSL with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d tsprtg.com -d www.tsprtg.com

# Auto-renewal is configured automatically
```

### 8. Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Maintenance

### View Logs

```bash
# Backend logs
sudo journalctl -u tsprtg-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Update Application

```bash
cd /opt/tsprtg
sudo git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart tsprtg-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

### Backup Database

```bash
# SQLite
cp /opt/tsprtg/backend/tsprtg.db /backup/tsprtg.db.$(date +%Y%m%d)

# PostgreSQL
pg_dump tsprtg > /backup/tsprtg.sql.$(date +%Y%m%d)
```

## Monitoring

Consider setting up:
- Log rotation for application logs
- Database backup automation
- Uptime monitoring (UptimeRobot, Pingdom, etc.)
- Error tracking (Sentry)
- Performance monitoring (New Relic, DataDog)

## Security Checklist

- [ ] Change default ADMIN_TOKEN in .env
- [ ] Configure firewall (ufw)
- [ ] Enable SSL/TLS (Let's Encrypt)
- [ ] Set up regular database backups
- [ ] Configure log rotation
- [ ] Keep system packages updated
- [ ] Review Nginx security headers
- [ ] Implement rate limiting (if needed)
- [ ] Regular security audits

## Troubleshooting

### Backend won't start
```bash
sudo systemctl status tsprtg-backend
sudo journalctl -u tsprtg-backend -n 50
```

### Database connection errors
- Check DATABASE_URL in .env
- Verify database exists and user has permissions
- Check PostgreSQL service is running

### Nginx errors
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

## Support

For issues and questions, please open a GitHub issue.
