# Deployment Guide 🚀

This guide covers deploying the AI Content Explorer to various environments.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git
- Docker (optional)

## Local Development

### 1. Quick Setup
```bash
# Clone and setup
git clone <your-repo-url>
cd ai-content-explorer
python setup.py

# Start services
./start_backend.sh  # or start_backend.bat on Windows
./start_frontend.sh # or start_frontend.bat on Windows
```

### 2. Manual Setup
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd auth-ui
npm install
npm start
```

## Production Deployment

### Environment Variables

Create `.env` file in `backend/` directory:

```env
# Production Settings
DEBUG=False
APP_NAME=AI Content Explorer

# Database
DATABASE_URL=postgresql://username:password@host:5432/database_name

# JWT
SECRET_KEY=your-very-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
TAVILY_API_KEY=your-tavily-api-key
FLUX_API_TOKEN=your-flux-api-token

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Database Setup

1. **Create PostgreSQL Database**
```sql
CREATE DATABASE ai_content_explorer;
CREATE USER ai_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ai_content_explorer TO ai_user;
```

2. **Run Migrations**
```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

### Backend Deployment

#### Option 1: Gunicorn + Nginx

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Create Gunicorn Config**
```bash
# backend/gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 2
```

3. **Start with Gunicorn**
```bash
gunicorn -c gunicorn.conf.py app.main:app
```

4. **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Option 2: Docker

1. **Create Dockerfile**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Run**
```bash
docker build -t ai-content-explorer-backend .
docker run -p 8000:8000 --env-file .env ai-content-explorer-backend
```

### Frontend Deployment

#### Option 1: Build and Serve

1. **Build Production Bundle**
```bash
cd auth-ui
npm run build
```

2. **Serve with Nginx**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/ai-content-explorer;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Option 2: Docker

1. **Create Dockerfile**
```dockerfile
# auth-ui/Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

2. **Build and Run**
```bash
docker build -t ai-content-explorer-frontend .
docker run -p 80:80 ai-content-explorer-frontend
```

## Docker Compose (Full Stack)

Create `docker-compose.yml` in the root directory:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: ai_content_explorer
      POSTGRES_USER: ai_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://ai_user:secure_password@postgres:5432/ai_content_explorer
    depends_on:
      - postgres
    ports:
      - "8000:8000"

  frontend:
    build: ./auth-ui
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

## SSL/HTTPS Setup

### Let's Encrypt with Certbot

1. **Install Certbot**
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain Certificate**
```bash
sudo certbot --nginx -d yourdomain.com
```

3. **Auto-renewal**
```bash
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### Health Checks

Add health check endpoint to your backend:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### Logging

Configure logging in `backend/app/core/config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Process Management

Use systemd for Linux:

```ini
# /etc/systemd/system/ai-content-explorer.service
[Unit]
Description=AI Content Explorer Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app/backend
Environment=PATH=/path/to/your/app/backend/.venv/bin
ExecStart=/path/to/your/app/backend/.venv/bin/gunicorn -c gunicorn.conf.py app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-content-explorer
sudo systemctl start ai-content-explorer
```

## Performance Optimization

### Backend

1. **Database Connection Pooling**
```python
# In your database configuration
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

2. **Caching with Redis**
```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expire_time=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expire_time, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### Frontend

1. **Code Splitting**
```javascript
// Use React.lazy for route-based code splitting
const Dashboard = React.lazy(() => import('./components/Dashboard'));
```

2. **Service Worker for Caching**
```javascript
// Register service worker for offline support
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Rotate keys regularly
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: Validate all user inputs
6. **SQL Injection**: Use parameterized queries
7. **CORS**: Configure CORS properly for production

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL service status
   - Verify connection string
   - Check firewall settings

2. **Frontend Build Fails**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify environment variables

3. **Backend Won't Start**
   - Check virtual environment activation
   - Verify all dependencies installed
   - Check port availability

### Logs

Check logs for errors:
```bash
# Backend logs
tail -f backend/app.log

# System logs
sudo journalctl -u ai-content-explorer -f

# Docker logs
docker-compose logs -f backend
```

## Support

For deployment issues:
- Check the logs
- Verify environment variables
- Test locally first
- Open an issue on GitHub
