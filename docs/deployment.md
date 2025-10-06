# Deployment Guide

## Overview

This guide covers deploying PROJECT NIV to production environments for both frontend (Next.js) and backend (FastAPI) components.

## Frontend Deployment (Next.js)

### Vercel (Recommended)

1. **Connect Repository**
   - Go to [Vercel](https://vercel.com)
   - Import your GitHub repository
   - Configure build settings

2. **Environment Variables**
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-domain.com
   ```

3. **Build Settings**
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

4. **Deploy**
   - Vercel automatically deploys on git push
   - Custom domains can be configured

### Netlify

1. **Connect Repository**
   - Go to [Netlify](https://netlify.com)
   - Connect your GitHub repository

2. **Build Settings**
   ```yaml
   build_command: npm run build
   publish_directory: .next
   ```

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` in Netlify dashboard

### Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY . .
   RUN npm run build
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

2. **Build and Run**
   ```bash
   docker build -t project-niv-frontend .
   docker run -p 3000:3000 project-niv-frontend
   ```

## Backend Deployment (FastAPI)

### Railway

1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository
   - Select the backend directory

2. **Environment Variables**
   ```env
   DATA_DIR=./data
   OUTPUT_DIR=./reports
   ```

3. **Deploy**
   - Railway automatically detects Python and installs dependencies
   - Service will be available at provided URL

### Render

1. **Create Web Service**
   - Go to [Render](https://render.com)
   - Create new Web Service
   - Connect GitHub repository

2. **Configuration**
   ```yaml
   Build Command: pip install -r backend/requirements.txt
   Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**
   - Add required environment variables

### Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt
   COPY backend/ .
   EXPOSE 8000
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and Run**
   ```bash
   docker build -t project-niv-backend .
   docker run -p 8000:8000 project-niv-backend
   ```

### Docker Compose

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     frontend:
       build: .
       ports:
         - "3000:3000"
       environment:
         - NEXT_PUBLIC_API_URL=http://backend:8000
       depends_on:
         - backend
     
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       volumes:
         - ./data:/app/data
         - ./reports:/app/reports
   ```

2. **Deploy**
   ```bash
   docker-compose up -d
   ```

## Environment Configuration

### Production Environment Variables

#### Frontend
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

#### Backend
```env
DATA_DIR=/app/data
OUTPUT_DIR=/app/reports
DEBUG=false
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Database Integration (Future)

### PostgreSQL Setup
```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
```

### Environment Variables
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Monitoring and Logging

### Application Monitoring
- Use services like DataDog, New Relic, or Sentry
- Monitor API response times and error rates
- Set up alerts for critical issues

### Logging
```python
# backend/logging.py
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
```

## Security Considerations

### HTTPS
- Always use HTTPS in production
- Configure SSL certificates
- Use secure headers

### CORS Configuration
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Environment Variables
- Never commit sensitive data
- Use secure environment variable management
- Rotate secrets regularly

## Performance Optimization

### Frontend
- Enable Next.js production optimizations
- Use CDN for static assets
- Implement caching strategies
- Optimize images and fonts

### Backend
- Use production ASGI server (Gunicorn + Uvicorn)
- Implement caching (Redis)
- Optimize database queries
- Use connection pooling

## Backup and Recovery

### Data Backup
```bash
# Backup data directory
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Backup reports
tar -czf reports-backup-$(date +%Y%m%d).tar.gz reports/
```

### Database Backup (Future)
```bash
# PostgreSQL backup
pg_dump -h localhost -U user dbname > backup.sql

# Restore
psql -h localhost -U user dbname < backup.sql
```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS configuration
   - Verify allowed origins

2. **API Connection Issues**
   - Check environment variables
   - Verify backend is running
   - Check network connectivity

3. **Build Failures**
   - Check Node.js and Python versions
   - Verify all dependencies are installed
   - Check for TypeScript errors

### Logs
```bash
# Frontend logs (Vercel)
vercel logs

# Backend logs (Railway)
railway logs

# Docker logs
docker logs container-name
```

## Scaling

### Horizontal Scaling
- Use load balancers
- Implement database clustering
- Use CDN for static assets
- Consider microservices architecture

### Vertical Scaling
- Increase server resources
- Optimize application performance
- Implement caching strategies