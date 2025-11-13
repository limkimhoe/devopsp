#!/bin/bash
# Flask startup script that ensures .env DATABASE_URL is used

# Clear any system-level DATABASE_URL to prevent override
unset DATABASE_URL

# Load environment variables from .env file
if [ -f .env ]; then
    echo "📁 Loading environment variables from .env..."
    set -a  # Automatically export all variables
    source .env
    set +a  # Stop auto-exporting
else
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Verify DATABASE_URL was loaded
if [ -z "$DATABASE_URL" ]; then
    echo "❌ Error: DATABASE_URL not found in .env file!"
    exit 1
fi

# Check if it's pointing to NeonDB
if [[ "$DATABASE_URL" == *"neondb_owner"* ]]; then
    echo "✅ Using NeonDB connection"
else
    echo "⚠️  Warning: DATABASE_URL may not be pointing to NeonDB"
fi

export FLASK_APP=project_flask

echo "🚀 Starting Flask application..."
echo "📡 Database: ${DATABASE_URL:0:50}..."
echo "🌐 Environment: ${FLASK_ENV:-production}"
echo "🔧 Port: ${FLASK_RUN_PORT:-5000}"
echo ""

# Start Flask
python -m flask run --host=0.0.0.0 --port=${FLASK_RUN_PORT:-5000}
