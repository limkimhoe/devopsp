"""
Gunicorn configuration file to prevent worker timeouts.
"""

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 60  # Increased from default 30 seconds
keepalive = 2

# Restart workers after this many requests (to prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Preload app for better memory usage
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'project_flask'

# Graceful restarts
graceful_timeout = 30
