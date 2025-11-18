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

# Test Database (Neon PostgreSQL)
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

#### For Testing (Neon PostgreSQL):

The testing database will be automatically set up during test runs. Ensure your Neon database is accessible.

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

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.0.x/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

---

## 🎯 Quick Reference

```bash
# Most common commands
pytest tests/ -v                    # Run all tests
pytest tests/ -m auth -v            # Run auth tests
pytest tests/ --cov=project_flask   # Run with coverage
pytest tests/ -k "login" -v         # Run tests matching "login"
pytest tests/ -x                    # Stop on first failure
```

This testing setup provides comprehensive coverage for your Flask application with proper environment separation and database configuration. Follow these instructions to maintain high code quality through automated testing.
