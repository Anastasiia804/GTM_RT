# TSPRTG Tag Manager - Quick Reference

## 🚀 Quick Start

```bash
# Run the quick start script
./start.sh

# Or start manually:
# Backend: cd backend && source venv/bin/activate && python run.py
# Frontend: cd frontend && npm run dev
```

## 📡 API Endpoints

### Base URLs
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

### Advertisers
```bash
# List advertisers
curl http://localhost:8000/api/advertisers

# Create advertiser
curl -X POST http://localhost:8000/api/advertisers \
  -H "Content-Type: application/json" \
  -d '{"name":"My Company","domains":["example.com"],"is_active":true}'

# Get advertiser
curl http://localhost:8000/api/advertisers/1

# Update advertiser
curl -X PUT http://localhost:8000/api/advertisers/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# Delete advertiser
curl -X DELETE http://localhost:8000/api/advertisers/1

# Get container code
curl http://localhost:8000/api/advertisers/1/code

# Get stats
curl http://localhost:8000/api/advertisers/1/stats
```

### Scripts
```bash
# List global scripts
curl http://localhost:8000/api/scripts

# Create global script
curl -X POST http://localhost:8000/api/scripts \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Analytics",
    "script_type":"external",
    "content":"https://example.com/script.js",
    "is_enabled":true,
    "priority":0,
    "is_async":true
  }'

# Toggle script
curl -X PATCH http://localhost:8000/api/scripts/1/toggle

# List advertiser scripts
curl http://localhost:8000/api/scripts/advertisers/1/scripts

# Create advertiser script
curl -X POST http://localhost:8000/api/scripts/advertisers/1/scripts \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Custom Script",
    "script_type":"inline",
    "content":"console.log(\"Hello\");",
    "is_enabled":true,
    "priority":1
  }'
```

### Container Loader (Public)
```bash
# Load container (needs valid referer)
curl -H "Referer: http://example.com/" \
  http://localhost:8000/c/adv_xxxxx/l.js
```

### Health Monitoring
```bash
# Overall health
curl http://localhost:8000/api/health

# All containers health
curl http://localhost:8000/api/health/containers

# Container logs
curl http://localhost:8000/api/health/containers/1/logs
```

## 🎨 Frontend Routes

- `/` - Dashboard
- `/advertisers` - Advertisers list
- `/advertisers/:id` - Advertiser details
- `/scripts` - Global scripts
- `/health` - Health monitoring

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up --build -d
```

## 🔧 Development Commands

### Backend
```bash
cd backend
source venv/bin/activate
python run.py                    # Start server
pip install -r requirements.txt  # Install deps
```

### Frontend
```bash
cd frontend
npm install          # Install deps
npm run dev          # Dev server
npm run build        # Production build
```

## 🧪 Testing

```bash
# Run API tests
./test-api.sh

# Test specific endpoint
curl http://localhost:8000/api/advertisers
```

## 📦 Database

### SQLite (Default)
- Location: `backend/tsprtg.db`
- View: `sqlite3 backend/tsprtg.db`

### Tables
- `advertisers` - Advertiser configurations
- `scripts` - Global and advertiser scripts
- `health_logs` - Container load logs

## 🔐 Security

### Environment Variables
Create `backend/.env`:
```
APP_NAME=TSPRTG Tag Manager
DATABASE_URL=sqlite:///./tsprtg.db
ADMIN_TOKEN=your-secret-token
CORS_ORIGINS=*
```

### Production Checklist
- [ ] Change ADMIN_TOKEN
- [ ] Configure proper CORS
- [ ] Use PostgreSQL
- [ ] Enable SSL/TLS
- [ ] Set up firewall
- [ ] Configure backups

## 📊 Container Status

- 🟢 **Active** - Loaded in last 24 hours
- 🟡 **Inactive** - Not loaded in 24+ hours
- 🔴 **Never** - Never been loaded

## 🎯 Script Types

### External Script
```json
{
  "script_type": "external",
  "content": "https://example.com/script.js"
}
```

### Inline Script
```json
{
  "script_type": "inline",
  "content": "console.log('Hello World');"
}
```

## 📝 Container Embed Code

```html
<!-- TSPRTG Container -->
<script type="text/javascript">
(function(w,d,c){
    var r=d.readyState;
    if(r!=='interactive'&&r!=='complete'){
        return setTimeout(function(){arguments.callee(w,d,c)},100);
    }
    var s=d.createElement('script');
    s.async=true;
    s.src='//tsprtg.com/c/'+c+'/l.js?v='+(+new Date());
    (d.body||d.head).appendChild(s);
    w._tsprtg=w._tsprtg||{};
    w._tsprtg.cid=c;
})(window,document,'CONTAINER_ID');
</script>
```

## 🆘 Troubleshooting

### Backend won't start
```bash
cd backend
source venv/bin/activate
python run.py
# Check error messages
```

### Frontend build fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Database locked
```bash
# Stop all processes using DB
ps aux | grep python
kill <PID>
```

## 📚 Additional Resources

- Full Documentation: `README.md`
- Deployment Guide: `deployment/DEPLOYMENT.md`
- Contributing: `CONTRIBUTING.md`
- API Docs: `http://localhost:8000/docs`
