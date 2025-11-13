# Database Setup Instructions

## NeonDB Database Initialization

The database tables and initial data must be set up before starting the application to prevent Gunicorn worker timeouts.

### Step 1: Configure Environment Variables

Ensure your `.env` file has the correct NeonDB connection string:

```bash
# Database URL for NeonDB
DATABASE_URL=postgresql://neondb_owner:npg_0RILPQnYtF9Z@ep-cold-scene-a1q7voma-pooler.ap-southeast-1.aws.neon.tech/building_app?sslmode=require

# Admin User Credentials
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminPass123!
```

### Step 2: Initialize Database

Run the initialization script to create tables and seed initial data:

```bash
python scripts/init_db.py
```

This script will:
- ✅ Create all database tables
- ✅ Create required roles (admin, standard)
- ✅ Create the admin user with credentials from environment variables
- ✅ Assign admin role to the admin user

### Step 3: Start the Application

After successful database initialization, you can start the application:

```bash
# PRODUCTION (Recommended) - Docker containers
./docker-run-gunicorn.sh

# PRODUCTION (Recommended) - Regular environments  
gunicorn -c gunicorn.conf.py project_flask:app

# DEVELOPMENT ONLY - Docker containers
./docker-run-flask.sh

# DEVELOPMENT ONLY - Regular environments
./run_flask.sh
```

**Important**: 
- **Use Gunicorn for production** - Better performance, stability, and concurrent request handling
- **Use Flask dev server for development only** - Has auto-reload but not production-ready
- All scripts handle Docker environment variable overrides and read from `.env` file

## Verification

You can verify the database setup by:

1. **Test database connection:**
   ```bash
   python scripts/test_db_connection.py
   ```

2. **Login to the application:**
   - Email: `admin@example.com`
   - Password: `AdminPass123!`

## Important Notes

- **Security**: Change the admin password after first login
- **Production**: Use strong, unique credentials for production deployments
- **Manual Initialization**: Database initialization is now manual to prevent Gunicorn worker timeouts
- **One-time Setup**: The initialization script is idempotent - safe to run multiple times

## Flask vs Gunicorn - When to Use Which

### **Gunicorn (Production Server) - RECOMMENDED**
```bash
./docker-run-gunicorn.sh        # For Docker
gunicorn -c gunicorn.conf.py project_flask:app  # For regular environments
```

**Why Gunicorn?**
- ✅ **Production-ready** WSGI server
- ✅ **Multiple worker processes** for concurrent requests
- ✅ **Better performance** and memory management
- ✅ **Graceful restarts** and error handling
- ✅ **Configurable timeouts** (prevents worker hangs)
- ✅ **Process management** and monitoring

### **Flask Development Server - DEVELOPMENT ONLY**
```bash
./docker-run-flask.sh    # For Docker
./run_flask.sh           # For regular environments
```

**Why Flask Dev Server?**
- ✅ **Auto-reload** on code changes
- ✅ **Debug mode** with detailed error pages
- ✅ **Simpler startup** for development
- ❌ **Not production-ready** (single-threaded, not secure)

## Troubleshooting

### Database Connection Issues:
1. Verify the `DATABASE_URL` is correct
2. Check NeonDB connection limits and pooling settings
3. Ensure SSL requirements are met (`sslmode=require`)
4. Check firewall/network connectivity to NeonDB

### Environment Variable Cache Issues:
If `.env` changes don't take effect, run:
```bash
python scripts/clear_env_cache.py
```

### System-Level DATABASE_URL Override:
**Most Common Issue**: If your app connects to a local database instead of NeonDB:

**For Docker Containers:**
- Docker environment variables override `.env` files
- **Solution**: Use `./docker-run-flask.sh` (designed for Docker)
- This script unsets Docker PostgreSQL variables and loads from `.env`

**For Regular Environments:**
- System environment variables override `.env` files  
- **Solution**: Use `./run_flask.sh` (designed for regular environments)
- This script clears system DATABASE_URL and loads from `.env`

**Manual Fix** (if scripts don't work):
```bash
DATABASE_URL="your_neondb_url_here" FLASK_APP=project_flask python -m flask run
```

### Gunicorn Worker Timeouts:
- Use the provided `gunicorn.conf.py` configuration
- The configuration increases timeout to 60 seconds and optimizes worker settings
- For development, use: `./run_flask.sh`

### SSL Configuration Conflicts:
- Ensure `project_flask/config.py` doesn't override NeonDB's `sslmode=require`
- The `SQLALCHEMY_ENGINE_OPTIONS` should not force `sslmode=disable`

### Health Check Endpoints:
Test your database connection:
```bash
curl http://localhost:5000/health     # Basic app health
curl http://localhost:5000/health/db  # Database connection test
```
