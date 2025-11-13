#!/bin/bash
# Docker-specific Gunicorn startup script for NeonDB

echo "🐳 Docker Gunicorn startup with NeonDB..."

# Clear Docker PostgreSQL variables that interfere with .env
unset DATABASE_URL POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_HOST POSTGRES_PORT

# Load .env file to get the correct DATABASE_URL
if [ -f .env ]; then
    echo "📁 Loading DATABASE_URL from .env file..."
    # Extract DATABASE_URL from .env file
    NEW_DATABASE_URL=$(grep "^DATABASE_URL=" .env | cut -d'=' -f2- | sed 's/^"//' | sed 's/"$//')
    if [ -n "$NEW_DATABASE_URL" ]; then
        export DATABASE_URL="$NEW_DATABASE_URL"
        echo "✅ Loaded DATABASE_URL from .env"
    else
        echo "❌ Error: DATABASE_URL not found in .env file!"
        exit 1
    fi
else
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Check if it's pointing to NeonDB
if [[ "$DATABASE_URL" == *"neondb_owner"* ]]; then
    echo "✅ Using NeonDB connection"
else
    echo "⚠️  Warning: DATABASE_URL may not be pointing to NeonDB"
fi

echo "🚀 Starting Gunicorn (Production WSGI Server)..."
echo "📡 Database: ${DATABASE_URL:0:50}..."
echo "🔧 Config: gunicorn.conf.py"
echo "🌐 Binding: 0.0.0.0:8000"
echo ""

# Start Gunicorn with configuration file
exec gunicorn -c gunicorn.conf.py project_flask:app
