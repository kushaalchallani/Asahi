# Asahi Deployment Guide

## Overview

This guide documents the deployment configuration for Asahi, accounting for free-tier limitations and production considerations.

## Free-Tier Limitations

### Render (Backend)

- **Free tier puts the service to sleep** after 15 minutes of inactivity
- **First request after sleep** takes 30-60 seconds to "wake up" (cold start)
- **Database connections may drop** during sleep - implement connection retry logic
- **Solution**: Set up a keep-alive ping (cron job or external service) to prevent sleeping

### Supabase (Database)

- **Free tier has connection limits** - typically 2-3 concurrent connections
- **Database enters idle mode** after periods of inactivity
- **Solution**: Monitor connection pool and implement graceful reconnection

### Vercel (Frontend)

- **Free tier is suitable** - no cold starts for static sites
- **CDN caching** ensures fast global delivery
- **Solution**: None needed - Vercel free tier is well-suited for this use case

## Production Configuration

### 1. Environment Variables

#### Backend (.env on Render)

```env
# Database
DATABASE_URL=postgresql+psycopg://user:password@db_host:5432/asahi_prod

# Security
ASAHI_SECRET_KEY=your-32-character-secret-key

# CORS - add your production frontend URL
FRONTEND_URL=https://your-app.vercel.app

# Optional: Environment
ENV=production
```

#### Frontend (.env on Vercel)

```env
# Backend API URL
VITE_API_URL=https://your-backend-service.onrender.com

# Optional: Feature flags
VITE_FEATURE_SHOW_STREAKS=true
VITE_FEATURE_SHOW_INSIGHTS=true
```

### 2. Database Migration (Supabase)

```bash
# Set up Supabase connection
# Replace with your actual Supabase connection string
DATABASE_URL=postgresql+psycopg://postgres:password@db.xxx.supabase.co:5432/postgres

# Run migrations
alembic upgrade head
```

### 3. Render Service Configuration

**Build Command:**
```bash
cd backend && pip install -r requirements.txt
```

**Start Command:**
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables to set in Render dashboard:**
- `DATABASE_URL` - Full PostgreSQL connection string
- `ASAHI_SECRET_KEY` - Secret key for JWT signing
- `FRONTEND_URL` - Your Vercel app URL (for CORS)

### 4. Keeping the Backend Awake

**Option A: Cron-based ping**

Create a simple keep-alive service:

```python
# keep_alive.py
import requests
import time
import os

BACKEND_URL = "https://your-render-service.onrender.com/health"
API_KEY = os.getenv("RENDER_API_KEY")

def ping():
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    while True:
        ping()
        time.sleep(300)  # Ping every 5 minutes
```

**Option B: Render cron job**

Set up a cron job in the Render dashboard:
- URL: `https://your-render-service.onrender.com/health`
- Schedule: `*/5 * * * *` (every 5 minutes)

### 5. Supabase Free-Tier Considerations

**Connection Management:**

```python
# In backend/core/database.py - add connection retry
import tenacity

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type(Exception)
)
def get_db_session():
    # Your session logic here
    pass
```

**Idle Timeout:**

- Supabase free tier databases may disconnect after 300 seconds (5 minutes)
- Implement connection health checks before queries
- Use SQLAlchemy's `pool_pre_ping=True` engine parameter

### 6. Vercel Configuration

**Vercel Project Settings:**

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add:
   - `VITE_API_URL`: `https://your-render-service.onrender.com`
   - Any other feature flags or config

**Root Directory:** Leave blank (root of the repo)

**Framework Preset:** Vite

### 7. Health Check Endpoint

The `/health` endpoint is essential for keep-alive pings:

```python
# Already exists in backend/main.py
@app.get("/health")
def health():
    return {"status": "ok"}
```

Use this endpoint for:
- Render keep-alive pings
- Database connection health checks
- Deployment verification

## Troubleshooting

### Common Issues

1. **Service wakes up but returns 500**
   - Check that DATABASE_URL is correctly set
   - Verify database migrations have been run
   - Ensure ASAHI_SECRET_KEY is set

2. **CORS errors in production**
   - Add your Vercel URL to FRONTEND_URL in the backend .env
   - Redeploy the backend after changing CORS config

3. **Database connection failures**
   - Verify Supabase project is active
   - Check that the database user has proper permissions
   - Ensure connection string uses correct port (5432)

4. **Mission recommendations return empty**
   - Verify the ML model can load (check sklearn compatibility)
   - Ensure database has mission data seeded
   - Check that user has check-ins to base recommendations on

### Monitoring

- Set up uptime monitoring (UptimeRobot, Pingdom, etc.)
- Monitor the `/health` endpoint response time
- Track database connection pool usage
- Log keep-alive ping successes/failures

## Summary

| Component | Service | Free Tier Status | Action Required |
|-----------|---------|-----------------|-----------------|
| Frontend | Vercel | ✅ Suitable | Set VITE_API_URL env var |
| Backend | Render | ⚠️ Sleeps after inactivity | Set up keep-alive ping |
| Database | Supabase | ⚠️ Connection limits | Monitor connection pool |
| CI/CD | GitHub Actions | ✅ Configured | Review and adjust as needed |

## Quick Start Checklist

- [ ] Set DATABASE_URL in Render environment variables
- [ ] Set ASAHI_SECRET_KEY in Render environment variables
- [ ] Set FRONTEND_URL in Render environment variables (your Vercel URL)
- [ ] Set VITE_API_URL in Vercel environment variables (your Render URL)
- [ ] Run `alembic upgrade head` on the production database
- [ ] Seed the database with missions: `python scripts/seed_missions.py`
- [ ] Set up keep-alive ping for Render free tier
- [ ] Test the /health endpoint
- [ ] Deploy frontend to Vercel
- [ ] Test the full user flow