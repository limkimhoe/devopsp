"""
Test configuration and fixtures
"""
import os
import pytest
from dotenv import load_dotenv

# Load test environment
load_dotenv('.env.test')

from project_flask import create_app
from project_flask.extensions import db
from project_flask.models import User, Role, UserProfile, Building, RefreshToken
from project_flask.config import TestingConfig


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app(TestingConfig())
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default roles
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        
        yield app
        
        # Cleanup
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def db_session(app):
    """Create clean database session for each test"""
    with app.app_context():
        # Start a transaction
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Configure session to use the transaction
        db.session.configure(bind=connection)
        
        yield db.session
        
        # Rollback transaction
        transaction.rollback()
        connection.close()
        db.session.remove()


@pytest.fixture
def admin_role(db_session):
    """Get admin role"""
    return Role.query.filter_by(name='admin').first()


@pytest.fixture
def user_role(db_session):
    """Get user role"""
    return Role.query.filter_by(name='user').first()


@pytest.fixture
def test_user(db_session, user_role):
    """Create a test user"""
    from project_flask.utils.security import hash_password
    
    user = User(
        email='test@example.com',
        password_hash=hash_password('TestPass123!'),
        is_active=True,
        is_banned=False
    )
    user.roles.append(user_role)
    db_session.add(user)
    db_session.flush()  # This assigns the ID to user
    
    # Create profile
    profile = UserProfile(
        user_id=user.id,
        display_name='Test User',
        first_name='Test',
        last_name='User'
    )
    db_session.add(profile)
    db_session.commit()
    
    return user


@pytest.fixture
def admin_user(db_session, admin_role):
    """Create an admin user"""
    from project_flask.utils.security import hash_password
    
    user = User(
        email='admin@example.com',
        password_hash=hash_password('AdminPass123!'),
        is_active=True,
        is_banned=False
    )
    user.roles.append(admin_role)
    db_session.add(user)
    db_session.flush()  # This assigns the ID to user
    
    # Create profile
    profile = UserProfile(
        user_id=user.id,
        display_name='Admin User',
        first_name='Admin',
        last_name='User'
    )
    db_session.add(profile)
    db_session.commit()
    
    return user


@pytest.fixture
def inactive_user(db_session, user_role):
    """Create an inactive user"""
    from project_flask.utils.security import hash_password
    
    user = User(
        email='inactive@example.com',
        password_hash=hash_password('TestPass123!'),
        is_active=False,
        is_banned=False
    )
    user.roles.append(user_role)
    db_session.add(user)
    db_session.flush()
    
    # Create profile for inactive user too
    profile = UserProfile(
        user_id=user.id,
        display_name='Inactive User',
        first_name='Inactive',
        last_name='User'
    )
    db_session.add(profile)
    db_session.commit()
    
    return user


@pytest.fixture
def banned_user(db_session, user_role):
    """Create a banned user"""
    from project_flask.utils.security import hash_password
    
    user = User(
        email='banned@example.com',
        password_hash=hash_password('TestPass123!'),
        is_active=True,
        is_banned=True,
        banned_reason='Test ban'
    )
    user.roles.append(user_role)
    db_session.add(user)
    db_session.flush()
    
    # Create profile for banned user too
    profile = UserProfile(
        user_id=user.id,
        display_name='Banned User',
        first_name='Banned',
        last_name='User'
    )
    db_session.add(profile)
    db_session.commit()
    
    return user


@pytest.fixture
def test_building(db_session):
    """Create a test building"""
    building = Building(
        name='Test Building',
        gml_file_path='/test/path/building.gml',
        texture_file_path='/test/path/texture.tif',
        xml_data='<test>xml</test>'
    )
    db_session.add(building)
    db_session.commit()
    
    return building


@pytest.fixture
def auth_headers(client, test_user):
    """Generate auth headers for test user"""
    response = client.post('/api/auth/login', json={
        'email': test_user.email,
        'password': 'TestPass123!'
    })
    
    if response.status_code == 200:
        access_token = response.json['access_token']
        return {'Authorization': f'Bearer {access_token}'}
    
    return {}


@pytest.fixture
def admin_auth_headers(client, admin_user):
    """Generate auth headers for admin user"""
    response = client.post('/api/auth/login', json={
        'email': admin_user.email,
        'password': 'AdminPass123!'
    })
    
    if response.status_code == 200:
        access_token = response.json['access_token']
        return {'Authorization': f'Bearer {access_token}'}
    
    return {}
