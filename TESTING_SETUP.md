# Flask Project Testing Setup Guide

This guide provides step-by-step instructions for setting up and running pytest tests for the Flask project, including authentication, user management, and building module testing.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Configuration](#database-configuration)
4. [Installation Steps](#installation-steps)
5. [Running Tests](#running-tests)
6. [Test Structure](#test-structure)
7. [Writing Custom Tests](#writing-custom-tests)
8. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

Before setting up the testing environment, ensure you have:

- Python 3.11 or higher
- PostgreSQL installed locally (for development)
- Access to Neon PostgreSQL (for testing)
- Git (for version control)
- Virtual environment tool (venv, conda, etc.)

## 🌍 Environment Setup

### 1. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd project_flask

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install all dependencies including testing packages
pip install -r requirements.txt
```

## 🗄️ Database Configuration

### Development Database (.env.development)

Create or verify your `.env.development` file:

```env
# Flask Development Environment
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
SECRET_KEY=dev-secret-change-me

# Local Development Database
POSTGRES_USER=appuser
POSTGRES_PASSWORD=appsecret
POSTGRES_DB=test_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg2://appuser:appsecret@localhost:5432/test_db

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_PRIVATE_KEY=dev-jwt-secret-key
JWT_PUBLIC_KEY=dev-jwt-secret-key

# Token lifetimes (seconds)
JWT_ACCESS_EXPIRES_SECONDS=900
JWT_REFRESH_EXPIRES_SECONDS=2592000

# Other settings...
```

### Testing Database (.env.test)

Your `.env.test` file should contain:

```env
# Flask Test Environment
FLASK_ENV=testing
FLASK_DEBUG=0
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5001
SECRET_KEY=test-secret-key-for-testing

# Test Database (Neon PostgreSQL for testing)
DATABASE_URL=postgresql://neondb_owner:npg_0RILPQnYtF9Z@ep-cold-scene-a1q7voma-pooler.ap-southeast-1.aws.neon.tech/test_db?sslmode=require

# JWT for testing
JWT_ALGORITHM=HS256
JWT_PRIVATE_KEY=test-jwt-secret-key-for-testing-only
JWT_PUBLIC_KEY=test-jwt-secret-key-for-testing-only

# Token lifetimes (shorter for testing)
JWT_ACCESS_EXPIRES_SECONDS=300
JWT_REFRESH_EXPIRES_SECONDS=3600

# Other testing settings...
```

**Note:** The test configuration automatically overrides the database URL to use SQLite in-memory for fast, isolated testing. The Neon PostgreSQL URL in `.env.test` is available for integration testing if needed.

### 3. Database Setup

#### For Development (Local PostgreSQL):

```bash
# Create local PostgreSQL database
createdb test_db

# Run database migrations
flask db upgrade

# Seed initial data (optional)
python scripts/seed_admin.py
```

#### For Testing:

**Tests use SQLite in-memory database automatically** - no manual setup required! The test configuration in `tests/conftest.py` automatically:
- Creates SQLite in-memory database for each test session
- Sets up all tables using `db.create_all()`
- Creates default roles (admin, user)
- Provides clean database state for each test
- Handles proper cleanup after tests

This provides:
✅ **Fast test execution** (no network calls)
✅ **Perfect isolation** between tests
✅ **No external dependencies** for testing
✅ **Automatic setup/teardown**

## 🚀 Installation Steps

### 1. Verify Environment Files

```bash
# Check if environment files exist
ls -la .env*

# Should show:
# .env
# .env.development  
# .env.test
```

### 2. Test Database Connection

```bash
# Test development database connection
python scripts/test_db_connection.py

# Test with specific environment
FLASK_ENV=testing python scripts/test_db_connection.py
```

### 3. Initialize Test Database

```bash
# Run a simple test to verify setup
pytest tests/test_auth.py::TestAuthLogin::test_login_invalid_email -v
```

## 🧪 Running Tests

### Basic Test Commands

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage report
pytest tests/ --cov=project_flask --cov-report=html

# Run tests and generate coverage report in terminal
pytest tests/ --cov=project_flask --cov-report=term-missing
```

### Run Tests by Module

```bash
# Authentication tests only
pytest tests/ -m auth -v

# User management tests only  
pytest tests/ -m user -v

# Building module tests only
pytest tests/ -m building -v

# Unit tests only
pytest tests/ -m unit -v

# Integration tests only
pytest tests/ -m integration -v
```

### Run Specific Test Classes or Functions

```bash
# Run specific test class
pytest tests/test_auth.py::TestAuthLogin -v

# Run specific test function
pytest tests/test_auth.py::TestAuthLogin::test_login_success -v

# Run tests matching pattern
pytest tests/ -k "login" -v
```

### Advanced Test Options

```bash
# Run tests in parallel (if pytest-xdist installed)
pytest tests/ -n 4

# Stop on first failure
pytest tests/ -x

# Show local variables in tracebacks
pytest tests/ -l

# Run tests with specific markers
pytest tests/ -m "auth and unit" -v

# Run tests with custom verbosity
pytest tests/ -vv  # Extra verbose
pytest tests/ -q   # Quiet mode
```

## 📁 Test Structure

### Directory Structure

```
tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Test configuration and fixtures
├── test_auth.py             # Authentication module tests
├── test_user_management.py  # User management tests
└── test_building_module.py  # Building module tests
```

### Test Categories

#### 1. Authentication Tests (`test_auth.py`)
- **Login Tests**: Valid/invalid credentials, banned users, inactive users
- **Token Tests**: Token generation, validation, refresh, expiration
- **Logout Tests**: Single logout, logout all sessions
- **Security Tests**: Token reuse detection, invalid token handling

#### 2. User Management Tests (`test_user_management.py`)
- **Service Tests**: User CRUD operations, profile management
- **Admin Endpoint Tests**: User creation, listing, modification, banning
- **Me Endpoint Tests**: Self-profile viewing and updating
- **Authorization Tests**: Role-based access control

#### 3. Building Module Tests (`test_building_module.py`)
- **Service Tests**: Building CRUD operations, file handling
- **Upload Tests**: GML and texture file validation
- **API Tests**: Building management endpoints
- **Image Processing**: Texture file serving as PNG

### Test Fixtures

Available in `conftest.py`:

- `app`: Flask application instance
- `client`: Test client for HTTP requests
- `db_session`: Database session with transaction rollback
- `test_user`: Regular user for testing
- `admin_user`: Admin user for testing
- `banned_user`: Banned user for testing
- `inactive_user`: Inactive user for testing
- `test_building`: Sample building for testing
- `auth_headers`: Authentication headers for regular user
- `admin_auth_headers`: Authentication headers for admin user

## ✍️ Writing Custom Tests

### Test Function Template

```python
import pytest
from project_flask.models import User

@pytest.mark.user  # Custom marker
@pytest.mark.unit  # Test type marker
def test_your_function(db_session, test_user):
    """Test description"""
    # Arrange
    expected_result = "expected value"
    
    # Act
    result = your_function(test_user)
    
    # Assert
    assert result == expected_result
    assert test_user.some_property == "some value"
```

### Integration Test Template

```python
@pytest.mark.user
@pytest.mark.integration
def test_api_endpoint(client, auth_headers):
    """Test API endpoint"""
    # Arrange
    payload = {"key": "value"}
    
    # Act
    response = client.post('/api/endpoint', 
                          headers=auth_headers, 
                          json=payload)
    
    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert data['key'] == 'expected_value'
```

### Adding New Test Markers

Add to `pytest.ini`:

```ini
[tool:pytest]
markers =
    auth: Authentication related tests
    user: User management tests
    building: Building module tests
    unit: Unit tests
    integration: Integration tests
    your_marker: Your custom marker description
```

## 🔍 Test Configuration

### pytest.ini Configuration

```ini
[tool:pytest]
minversion = 7.0
addopts = 
    -ra 
    --strict-markers 
    --strict-config 
    --disable-warnings
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    auth: Authentication related tests
    user: User management tests  
    building: Building module tests
    unit: Unit tests
    integration: Integration tests
```

### Environment Variables for Testing

```bash
# Set specific environment for tests
export FLASK_ENV=testing

# Run tests with environment file
pytest tests/ --env-file=.env.test -v

# Override database for testing
export DATABASE_URL=your_test_database_url
pytest tests/ -v
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Errors

```bash
# Error: could not connect to server
# Solution: Check if PostgreSQL is running
sudo service postgresql start  # Linux
brew services start postgresql  # Mac

# Verify connection manually
psql -h localhost -U appuser -d test_db
```

#### 2. Import Errors

```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in the project root and virtual environment is activated
pwd  # Should be in project root
which python  # Should point to venv
pip list | grep Flask  # Verify Flask is installed
```

#### 3. Test Database Issues

```bash
# Error: relation does not exist
# Solution: Run database migrations for test environment
FLASK_ENV=testing flask db upgrade

# Clear test database and restart
FLASK_ENV=testing flask db downgrade base
FLASK_ENV=testing flask db upgrade
```

#### 4. Authentication Test Failures

```bash
# Error: Invalid JWT token
# Solution: Check JWT configuration in .env.test
# Ensure JWT_PRIVATE_KEY and JWT_PUBLIC_KEY are set correctly
```

#### 5. Permission Denied Errors

```bash
# Error: permission denied for relation
# Solution: Check database user permissions
# Grant necessary permissions to test user
GRANT ALL PRIVILEGES ON DATABASE test_db TO appuser;
```

### Debug Test Failures

```bash
# Run failed tests with maximum verbosity
pytest tests/test_failed.py::test_function -vvv

# Show local variables in failure
pytest tests/test_failed.py::test_function -l

# Start debugger on failure
pytest tests/test_failed.py::test_function --pdb

# Show print statements
pytest tests/test_failed.py::test_function -s
```

### Logging During Tests

Add to your test function:

```python
import logging

def test_with_logging(caplog):
    with caplog.at_level(logging.INFO):
        # Your test code
        result = some_function()
    
    # Check logs
    assert "Expected log message" in caplog.text
```

## ✅ Current Test Status

### Test Suite Overview

**All tests are currently passing** ✅

```bash
# Latest test results (as of November 2024)
======================== 106 passed, 102 warnings in 10.04s ========================

# Test breakdown by module:
- Authentication Tests: 22 tests ✅
- User Management Tests: 23 tests ✅  
- Building Module Tests: 61 tests ✅
```

### Recent Fixes Applied

The testing infrastructure has been updated with the following critical fixes:

#### 1. JWT Token Error Handling ✅
- **Issue**: Malformed JWT tokens caused 500 errors instead of proper 401 responses
- **Fix**: Updated `auth_service.py` to catch `DecodeError` and raise `ValueError("invalid_token")`
- **Impact**: Improved error handling in `test_refresh_invalid_token` and related tests

#### 2. User Management Error Handling ✅
- **Issue**: Duplicate email constraints caused unhandled `IntegrityError`
- **Fix**: Added proper error handling in `user_service.py` and `admin_users.py`
- **Impact**: Tests now properly validate 409 Conflict responses for duplicate emails

#### 3. Building Module Test Fixes ✅
- **Issue**: Test patches and mock objects were incorrectly configured
- **Fix**: 
  - Corrected patch paths to patch imports, not definitions
  - Fixed mock building objects to have proper datetime fields
  - Updated edge case error handling tests
- **Impact**: All 61 building module tests now pass consistently

#### 4. Test Configuration ✅
- **Status**: pytest.ini properly configured with custom markers
- **Markers**: `auth`, `user`, `building`, `unit`, `integration`
- **Environment**: Automatic SQLite in-memory database setup

### Test Categories and Coverage

```bash
# Run tests by category
pytest tests/ -m auth -v          # 22 authentication tests
pytest tests/ -m user -v          # 23 user management tests  
pytest tests/ -m building -v      # 61 building module tests
pytest tests/ -m unit -v          # Unit tests across all modules
pytest tests/ -m integration -v   # Integration tests across all modules
```

## 📊 Coverage Reports

### Generate HTML Coverage Report

```bash
# Run tests with coverage
pytest tests/ --cov=project_flask --cov-report=html

# Open coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
# On Windows: start htmlcov/index.html
```

### Current Coverage Metrics

The test suite provides comprehensive coverage across:

- **Authentication Module**: Login, logout, token management, security validation
- **User Management**: CRUD operations, admin functions, profile management, role-based access
- **Building Module**: File uploads, building management, texture processing, error handling
- **Edge Cases**: Error conditions, validation failures, security scenarios
- **Integration**: End-to-end API testing with proper authentication flows

### Coverage Configuration

Create `.coveragerc`:

```ini
[run]
source = project_flask
omit = 
    project_flask/config.py
    project_flask/__init__.py
    */migrations/*
    */venv/*
    tests/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🚀 Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/ --cov=project_flask
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
```

## 🐳 Docker Container Testing

### Docker Environment Overview

Your project supports both **local development** and **containerized development** with comprehensive testing capabilities in both environments.

#### Container Architecture

```
┌─────────────────────────────────────────┐
│  VS Code Dev Container                  │
│  ┌─────────────────────────────────────┐│
│  │  Flask App Container (devapp)       ││
│  │  - Python 3.11                     ││
│  │  - pytest + all dependencies       ││
│  │  - Live code mounting              ││
│  │  - Port 5000, 8888                 ││
│  └─────────────────────────────────────┘│
│                                         │
│  ┌─────────────────────────────────────┐│
│  │  PostgreSQL Container (devpg)       ││
│  │  - postgres:16                     ││
│  │  - Port 5434 (external)            ││
│  │  - Persistent data volume          ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

### 1. Dev Container Setup

#### Prerequisites for Container Development

```bash
# Required software
- Docker Desktop or Docker Engine
- VS Code with "Dev Containers" extension
- Git

# Optional but recommended
- Docker Compose (included with Docker Desktop)
```

#### Opening Project in Dev Container

```bash
# Method 1: VS Code Command Palette
# 1. Open VS Code
# 2. Ctrl/Cmd + Shift + P
# 3. Type: "Dev Containers: Reopen in Container"
# 4. Wait for container build and setup

# Method 2: From command line
code .
# Then use Command Palette as above

# Method 3: Direct container startup
cd /workspace
docker-compose -f .devcontainer/docker-compose.yml up -d
docker exec -it devapp bash
```

#### Container Service Management

```bash
# Start all services
docker-compose -f .devcontainer/docker-compose.yml up -d

# Check service status
docker-compose -f .devcontainer/docker-compose.yml ps

# View logs
docker-compose -f .devcontainer/docker-compose.yml logs app
docker-compose -f .devcontainer/docker-compose.yml logs db

# Stop all services
docker-compose -f .devcontainer/docker-compose.yml down

# Rebuild containers (after dependency changes)
docker-compose -f .devcontainer/docker-compose.yml up --build -d
```

### 2. Running Tests in Containers

#### Inside Dev Container (Recommended)

When working in VS Code dev container, tests run directly in the Flask app container:

```bash
# Basic test commands (same as local)
pytest tests/ -v                    # All tests
pytest tests/ -m auth -v            # Auth tests only
pytest tests/ -m user -v            # User management tests
pytest tests/ -m building -v        # Building module tests

# Container-optimized commands
pytest tests/ --maxfail=5 -v        # Stop after 5 failures
pytest tests/ --tb=short -v         # Shorter tracebacks
pytest tests/ -x --lf              # Stop on first failure, run last failed
```

#### From Host Machine

Run tests in container from outside:

```bash
# Execute tests in running container
docker exec -it devapp pytest tests/ -v

# Run specific test modules
docker exec -it devapp pytest tests/test_auth.py -v

# Run with coverage
docker exec -it devapp pytest tests/ --cov=project_flask --cov-report=html

# Interactive shell for debugging
docker exec -it devapp bash
# Then run pytest commands inside container
```

#### One-off Container Testing

```bash
# Run tests in fresh container (database isolated)
docker run --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  --env-file .env.test \
  python:3.11-slim \
  bash -c "pip install -r requirements.txt && pytest tests/ -v"
```

### 3. Container Database Testing

#### Database Options in Containers

**Option 1: SQLite In-Memory (Default for Tests)**
```bash
# Automatic - no setup required
# Tests use SQLite regardless of container PostgreSQL
pytest tests/ -v
```

**Option 2: Container PostgreSQL for Integration Tests**
```bash
# Create test database in container PostgreSQL
docker exec -it devpg createdb -U appuser test_integration_db

# Run tests against container database
export DATABASE_URL="postgresql://appuser:appsecret@localhost:5434/test_integration_db"
pytest tests/ -v --tb=short
```

**Option 3: Separate Test Database Container**
```yaml
# Add to .devcontainer/docker-compose.yml
  testdb:
    image: postgres:16
    container_name: testpg
    environment:
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
      POSTGRES_DB: testdb
    ports:
      - "5435:5432"
    tmpfs:
      - /var/lib/postgresql/data  # In-memory database
```

### 4. Container Testing Workflows

#### Development Testing Workflow

```bash
# 1. Start dev container
code .  # Open in VS Code, reopen in container

# 2. Verify container setup
python --version  # Should be 3.11.x
pip list | grep pytest  # Verify pytest installed
which python  # Should be /usr/local/bin/python

# 3. Run tests to verify setup
pytest tests/test_auth.py::TestAuthLogin::test_login_success -v

# 4. Run full test suite
pytest tests/ -v

# 5. Generate coverage report
pytest tests/ --cov=project_flask --cov-report=html
# View at http://localhost:5000/htmlcov/index.html (if serving)
```

#### Continuous Testing Workflow

```bash
# Watch for changes and auto-run tests
# Install pytest-watch in container
pip install pytest-watch

# Watch and run tests on file changes
ptw tests/ -- -v --tb=short

# Watch specific modules
ptw tests/test_auth.py -- -v
```

#### Database Migration Testing in Container

```bash
# Test migrations in container PostgreSQL
export FLASK_APP=project_flask
export DATABASE_URL="postgresql://appuser:appsecret@db:5432/appdb"

# Test migration workflow
flask db upgrade
pytest tests/ -v
flask db downgrade
flask db upgrade
```

### 5. Docker-Specific Testing Commands

#### Container Health Checks

```bash
# Check if containers are healthy
docker-compose -f .devcontainer/docker-compose.yml ps

# Test database connectivity from app container
docker exec -it devapp python scripts/test_db_connection.py

# Test Flask app startup in container
docker exec -it devapp python -c "from project_flask import create_app; print('✅ Flask imports successfully')"

# Verify pytest configuration
docker exec -it devapp pytest --collect-only tests/
```

#### Performance Testing in Containers

```bash
# Run tests with timing
docker exec -it devapp pytest tests/ --durations=10 -v

# Memory usage monitoring
docker exec -it devapp pytest tests/ --profile -v

# Parallel test execution (if pytest-xdist installed)
docker exec -it devapp pytest tests/ -n auto -v
```

#### Container Log Analysis

```bash
# View test output with container logs
docker-compose -f .devcontainer/docker-compose.yml logs -f app &
pytest tests/ -v -s

# Capture test logs
docker exec -it devapp pytest tests/ -v --capture=no > test_output.log 2>&1
```

### 6. Environment Variables in Containers

#### Container Environment Management

```bash
# Check loaded environment in container
docker exec -it devapp env | grep -E "(FLASK|DATABASE|JWT)"

# Test environment file loading
docker exec -it devapp python -c "
import os
from dotenv import load_dotenv
load_dotenv('.env.test')
print(f'FLASK_ENV: {os.getenv(\"FLASK_ENV\")}')
print(f'DATABASE_URL: {os.getenv(\"DATABASE_URL\")[:50]}...')
"

# Override environment for specific tests
docker exec -it devapp bash -c "
export FLASK_ENV=testing
export DATABASE_URL='sqlite:///:memory:'
pytest tests/test_auth.py -v
"
```

### 7. Container Troubleshooting

#### Common Container Issues

**Issue 1: Container Build Failures**
```bash
# Clear Docker cache and rebuild
docker-compose -f .devcontainer/docker-compose.yml down --volumes
docker system prune -f
docker-compose -f .devcontainer/docker-compose.yml up --build -d

# Check build logs
docker-compose -f .devcontainer/docker-compose.yml logs app
```

**Issue 2: Database Connection Issues**
```bash
# Test database connectivity
docker exec -it devpg pg_isready -U appuser -d appdb

# Check database container health
docker inspect devpg --format='{{.State.Health.Status}}'

# Manual database connection test
docker exec -it devapp python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://appuser:appsecret@db:5432/appdb')
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
```

**Issue 3: Port Conflicts**
```bash
# Check port usage on host
netstat -tulpn | grep :5434
lsof -i :5434

# Use different ports in docker-compose.yml
# Change "5434:5432" to "5436:5432" for database
```

**Issue 4: Permission Issues**
```bash
# Check file permissions in container
docker exec -it devapp ls -la /workspace

# Fix permission issues
docker exec -it devapp chown -R vscode:vscode /workspace
```

**Issue 5: Test Database State Issues**
```bash
# Reset container database
docker exec -it devpg dropdb -U appuser --if-exists appdb
docker exec -it devpg createdb -U appuser appdb

# Or restart entire stack
docker-compose -f .devcontainer/docker-compose.yml restart
```

#### Debug Container Testing

```bash
# Interactive debugging session
docker exec -it devapp python -m pdb -m pytest tests/test_auth.py::test_login_success

# Install additional debugging tools in container
docker exec -it devapp pip install ipdb pytest-pdb
docker exec -it devapp pytest tests/ --pdb -v

# Container shell with full environment
docker exec -it devapp bash
# Then run individual commands for debugging
```

### 8. Container CI/CD Integration

#### GitHub Actions with Docker

```yaml
# .github/workflows/docker-test.yml
name: Docker Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and test in containers
        run: |
          docker-compose -f .devcontainer/docker-compose.yml up -d --build
          docker-compose -f .devcontainer/docker-compose.yml exec -T app pytest tests/ -v
          docker-compose -f .devcontainer/docker-compose.yml down
```

#### Production Container Testing

```bash
# Build production container
docker build -f project_flask/Dockerfile -t flask-app:test .

# Test production container
docker run --rm \
  --env-file .env.test \
  -v $(pwd)/tests:/app/tests \
  flask-app:test \
  pytest tests/ -v

# Multi-stage container testing
docker build --target test -f project_flask/Dockerfile -t flask-app:test-stage .
docker run --rm flask-app:test-stage pytest tests/ -v
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.0.x/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Docker Development Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

---

## 🎯 Quick Reference

### Local Testing
```bash
# Most common commands
pytest tests/ -v                    # Run all tests
pytest tests/ -m auth -v            # Run auth tests
pytest tests/ --cov=project_flask   # Run with coverage
pytest tests/ -k "login" -v         # Run tests matching "login"
pytest tests/ -x                    # Stop on first failure
```

### Container Testing
```bash
# Dev container (inside VS Code)
pytest tests/ -v                    # Same as local
pytest tests/ --tb=short -v         # Shorter tracebacks for containers

# From host machine
docker exec -it devapp pytest tests/ -v                    # All tests in container
docker exec -it devapp pytest tests/ --cov=project_flask   # Coverage in container

# Container management
docker-compose -f .devcontainer/docker-compose.yml up -d   # Start containers
docker-compose -f .devcontainer/docker-compose.yml logs app # View app logs
docker-compose -f .devcontainer/docker-compose.yml down    # Stop containers
```

This testing setup provides comprehensive coverage for your Flask application with both local and containerized development environments. The Docker integration ensures consistent testing environments across different development setups while maintaining the same high code quality standards.
