# TSPRTG Tag Manager

A comprehensive tag management system (similar to Google Tag Manager) for managing advertising tags and scripts across multiple domains. Built with FastAPI, SQLite, and Vue.js 3.

> **🔒 Security Notice**: All dependencies are up-to-date with latest security patches. See [SECURITY.md](SECURITY.md) for details.

## Features

- **Multi-Advertiser Support**: Manage multiple advertisers with unique container IDs
- **Domain Whitelisting**: Control which domains can load containers
- **Script Management**: Global and advertiser-specific scripts (external URLs or inline code)
- **Real-time Monitoring**: Health checks and activity logs for all containers
- **Container Code Generation**: Auto-generated embed codes for each advertiser
- **Priority-based Loading**: Control script execution order
- **CORS Support**: Load containers from any domain
- **Caching**: 5-minute cache for loader scripts

## Technology Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Vue.js 3, Vite, Pinia, Axios
- **Deployment**: Docker, Docker Compose, Nginx

## Project Structure

```
GTM_RT/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   └── schemas/             # Pydantic schemas
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── views/               # Vue pages
│   │   ├── components/          # Vue components
│   │   ├── router/              # Vue Router
│   │   ├── stores/              # Pinia stores
│   │   └── api/                 # API client
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for containerized deployment)

### Local Development Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run the backend
python run.py
```

The backend API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Nginx: `http://localhost:80`

## API Endpoints

### Advertisers

```
GET    /api/advertisers              # List all advertisers
POST   /api/advertisers              # Create advertiser
GET    /api/advertisers/{id}         # Get advertiser details
PUT    /api/advertisers/{id}         # Update advertiser
DELETE /api/advertisers/{id}         # Delete advertiser
GET    /api/advertisers/{id}/code    # Get container embed code
GET    /api/advertisers/{id}/stats   # Get container statistics
```

### Scripts

```
# Global Scripts
GET    /api/scripts                  # List global scripts
POST   /api/scripts                  # Create global script
GET    /api/scripts/{id}             # Get script
PUT    /api/scripts/{id}             # Update script
DELETE /api/scripts/{id}             # Delete script
PATCH  /api/scripts/{id}/toggle      # Toggle script status

# Advertiser Scripts
GET    /api/scripts/advertisers/{id}/scripts
POST   /api/scripts/advertisers/{id}/scripts
PUT    /api/scripts/advertisers/{adv_id}/scripts/{script_id}
DELETE /api/scripts/advertisers/{adv_id}/scripts/{script_id}
PATCH  /api/scripts/advertisers/{adv_id}/scripts/{script_id}/toggle
```

### Container Loader (Public)

```
GET    /c/{container_id}/l.js        # Load container JavaScript
```

### Health Monitoring

```
GET    /api/health                   # Overall system health
GET    /api/health/containers        # All containers health status
GET    /api/health/containers/{id}/logs  # Container activity logs
```

## Usage

### 1. Create an Advertiser

1. Navigate to "Advertisers" page
2. Click "Create Advertiser"
3. Enter name and allowed domains (e.g., `example.com`, `subdomain.example.com`)
4. Save

A unique container ID will be automatically generated (e.g., `adv_a1b2c3d4`)

### 2. Get Container Code

1. Open advertiser details
2. Copy the generated container code
3. Paste it into the `<head>` section of your website

Example container code:
```html
<!-- TSPRTG Container for: My Advertiser -->
<!-- Container ID: adv_a1b2c3d4 -->
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
})(window,document,'adv_a1b2c3d4');
</script>
<!-- End TSPRTG Container -->
```

### 3. Add Scripts

#### Global Scripts
Scripts that load for all advertisers:
- Navigate to "Global Scripts"
- Click "Add Global Script"
- Configure script (external URL or inline code)
- Set priority (lower numbers load first)

#### Advertiser-Specific Scripts
Scripts for a single advertiser:
- Open advertiser details
- Click "Add Script"
- Configure and save

### 4. Monitor Health

- Navigate to "Health Monitor"
- View real-time status of all containers
- Check load counts and last activity
- View detailed activity logs

**Status Indicators:**
- 🟢 **Active**: Loaded in last 24 hours
- 🟡 **Inactive**: Not loaded in last 24 hours
- 🔴 **Never Loaded**: Never been loaded

## Database Schema

### Advertisers Table
- `id`: Primary key
- `name`: Advertiser name
- `container_id`: Unique container identifier
- `domains`: JSON array of allowed domains
- `is_active`: Active status
- `created_at`, `updated_at`: Timestamps

### Scripts Table
- `id`: Primary key
- `advertiser_id`: FK to advertisers (NULL for global scripts)
- `name`: Script name
- `script_type`: 'external' or 'inline'
- `content`: URL or JavaScript code
- `is_enabled`: Enabled status
- `priority`: Load order (lower = first)
- `is_async`, `is_defer`: Script loading attributes
- `created_at`, `updated_at`: Timestamps

### Health Logs Table
- `id`: Primary key
- `container_id`: Container identifier
- `referer`: Request referer URL
- `ip_address`: Client IP
- `user_agent`: Client user agent
- `is_allowed`: Whether request passed domain check
- `created_at`: Timestamp

## Security Features

- Domain whitelisting to prevent unauthorized use
- Request logging for audit trails
- CORS configuration
- Admin token authentication (configurable in `.env`)

## Configuration

Edit `backend/.env`:

```env
APP_NAME=TSPRTG Tag Manager
DATABASE_URL=sqlite:///./tsprtg.db
ADMIN_TOKEN=your-secret-token-here
CORS_ORIGINS=*
```

## Production Deployment

1. Update `nginx.conf` with your domain
2. Configure SSL certificates
3. Set secure `ADMIN_TOKEN` in `.env`
4. Use production database (PostgreSQL recommended)
5. Build frontend: `cd frontend && npm run build`
6. Deploy with `docker-compose up -d`

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
python run.py
```

API auto-reloads on code changes.

### Frontend Development

```bash
cd frontend
npm run dev
```

Hot module replacement enabled.

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
