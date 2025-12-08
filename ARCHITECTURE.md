# System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         TSPRTG Tag Manager                       │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                           CLIENT WEBSITES                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐      │
│  │ example.com│  │  shop.com  │  │  blog.com  │  │  news.com  │      │
│  │            │  │            │  │            │  │            │      │
│  │ <script>   │  │ <script>   │  │ <script>   │  │ <script>   │      │
│  │ Container  │  │ Container  │  │ Container  │  │ Container  │      │
│  │   Code     │  │   Code     │  │   Code     │  │   Code     │      │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘      │
└────────┼───────────────┼───────────────┼───────────────┼──────────────┘
         │               │               │               │
         └───────────────┴───────────────┴───────────────┘
                                 │
                                 ▼
         ┌─────────────────────────────────────────┐
         │  /c/{container_id}/l.js (Loader API)   │
         │  • Domain Validation                    │
         │  • Script Injection                     │
         │  • Request Logging                      │
         │  • 5-min Cache                         │
         └─────────────┬───────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────────┐
│                      NGINX (Reverse Proxy)                       │
│  • SSL/TLS Termination                                           │
│  • Caching Layer                                                 │
│  • CORS Headers                                                  │
│  • Static File Serving                                           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌──────────────────┐        ┌────────────────────┐
│  FastAPI Backend │        │  Vue.js Frontend   │
│  (Port 8000)     │        │  (Port 3000)       │
│                  │        │                    │
│  ┌────────────┐  │        │  ┌──────────────┐ │
│  │  Routers   │  │        │  │  Dashboard   │ │
│  │            │  │        │  │  Advertisers │ │
│  │ • Advertisers│ │       │  │  Scripts     │ │
│  │ • Scripts  │  │        │  │  Health      │ │
│  │ • Loader   │  │        │  └──────────────┘ │
│  │ • Health   │  │        │                    │
│  └────┬───────┘  │        │  ┌──────────────┐ │
│       │          │        │  │  Components  │ │
│  ┌────▼───────┐  │        │  │              │ │
│  │  Services  │  │        │  │ • Navbar     │ │
│  │            │  │        │  │ • Cards      │ │
│  │ • Container│  │        │  │ • Editors    │ │
│  │   Generator│  │        │  │ • Stats      │ │
│  │ • Health   │  │        │  └──────────────┘ │
│  │   Checker  │  │        │                    │
│  └────┬───────┘  │        │  ┌──────────────┐ │
│       │          │        │  │  API Client  │ │
│  ┌────▼───────┐  │        │  │  (Axios)     │ │
│  │   Models   │  │        │  └──────┬───────┘ │
│  │            │  │        └─────────┼─────────┘
│  │ • Advertiser│ │                  │
│  │ • Script   │  │                  │
│  │ • HealthLog│  │                  │
│  └────┬───────┘  │                  │
│       │          │                  │
│  ┌────▼───────┐  │◄─────────────────┘
│  │  Database  │  │   HTTP/JSON API
│  │  (SQLite)  │  │
│  │            │  │
│  │ Tables:    │  │
│  │ • advertisers │
│  │ • scripts  │  │
│  │ • health_logs │
│  └────────────┘  │
└──────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                      DATA FLOW                                  │
└────────────────────────────────────────────────────────────────┘

1. CONTAINER LOADING
   Client Website → Referer Header → Nginx → Backend Loader
   → Domain Validation → Script Generation → Minification
   → Cache → Response with JS → Client Executes Scripts

2. ADMIN OPERATIONS
   Admin UI → API Client → Nginx → Backend API
   → Database → Response → UI Update

3. HEALTH MONITORING
   Container Load → Log Creation → Database
   → Health API → Statistics Calculation → Dashboard Display

┌────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                              │
└────────────────────────────────────────────────────────────────┘

1. Domain Whitelisting - Referer validation
2. CORS Configuration - Controlled access
3. Input Validation - Pydantic schemas
4. SQL Injection Protection - ORM
5. Admin Authentication - Token-based
6. SSL/TLS - HTTPS only
7. Request Logging - Audit trail

┌────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                           │
└────────────────────────────────────────────────────────────────┘

Option 1: Docker Compose (Recommended)
┌─────────────────────────────────────────────┐
│  Docker Compose                             │
│  ├── Backend Container                      │
│  ├── Frontend Container                     │
│  └── Nginx Container                        │
└─────────────────────────────────────────────┘

Option 2: Traditional Server
┌─────────────────────────────────────────────┐
│  Linux Server                               │
│  ├── Systemd Service (Backend)             │
│  ├── Nginx (Static + Proxy)                │
│  └── Process Manager (PM2/Supervisor)      │
└─────────────────────────────────────────────┘

Option 3: Cloud Platform
┌─────────────────────────────────────────────┐
│  Cloud Service                              │
│  ├── Backend: Heroku/AWS/GCP/Azure         │
│  ├── Frontend: Vercel/Netlify/S3          │
│  └── Database: RDS/Cloud SQL               │
└─────────────────────────────────────────────┘
