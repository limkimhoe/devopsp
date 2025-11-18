"""
User management module tests
"""
import pytest
from datetime import datetime
from unittest.mock import patch

from project_flask.models import User, UserProfile, Role, UserRole
from project_flask.services.user_service import (
    create_user, get_user_by_id, update_user_admin, update_profile,
    list_users, ban_user, unban_user
)
from project_flask.utils.security import hash_password, verify_password


@pytest.mark.user
@pytest.mark.unit
class TestUserService:
    """Test user service functions"""

    def test_create_user_basic(self, db_session, user_role):
        """Test creating a basic user"""
        user = create_user(
            email="newuser@example.com",
            temp_password="TempPass123!",
            roles=["user"]
        )
        
        assert user.email == "newuser@example.com"
        assert verify_password("TempPass123!", user.password_hash)
        assert user.is_active is True
        assert user.is_banned is False
        assert len(user.roles) == 1
        assert user.roles[0].name == "user"

    def test_create_user_with_profile(self, db_session, user_role):
        """Test creating user with profile data"""
        profile_data = {
            "display_name": "New User",
            "first_name": "New",
            "last_name": "User",
            "phone": "+1234567890"
        }
        
        user = create_user(
            email="newuser@example.com",
            temp_password="TempPass123!",
            roles=["user"],
            profile_data=profile_data
        )
        
        assert user.profile is not None
        assert user.profile.display_name == "New User"
        assert user.profile.first_name == "New"
        assert user.profile.last_name == "User"
        assert user.profile.phone == "+1234567890"

    def test_create_user_multiple_roles(self, db_session, admin_role, user_role):
        """Test creating user with multiple roles"""
        user = create_user(
            email="multiuser@example.com",
            temp_password="TempPass123!",
            roles=["admin", "user"]
        )
        
        role_names = [r.name for r in user.roles]
        assert "admin" in role_names
        assert "user" in role_names

    def test_get_user_by_id_exists(self, db_session, test_user):
        """Test getting existing user by ID"""
        found_user = get_user_by_id(test_user.id)
        assert found_user is not None
        assert found_user.id == test_user.id
        assert found_user.email == test_user.email

    def test_get_user_by_id_not_exists(self, db_session):
        """Test getting non-existent user by ID"""
        found_user = get_user_by_id("non-existent-id")
        assert found_user is None

    def test_update_user_admin_email(self, db_session, test_user):
        """Test updating user email as admin"""
        updated_user = update_user_admin(
            test_user,
            email="updated@example.com"
        )
        
        assert updated_user.email == "updated@example.com"

    def test_update_user_admin_roles(self, db_session, test_user, admin_role):
        """Test updating user roles as admin"""
        updated_user = update_user_admin(
            test_user,
            roles=["admin", "user"]
        )
        
        role_names = [r.name for r in updated_user.roles]
        assert "admin" in role_names
        assert "user" in role_names

    def test_update_user_admin_active_status(self, db_session, test_user):
        """Test updating user active status as admin"""
        updated_user = update_user_admin(
            test_user,
            is_active=False
        )
        
        assert updated_user.is_active is False

    def test_update_profile_existing(self, db_session, test_user):
        """Test updating existing user profile"""
        profile_data = {
            "display_name": "Updated Name",
            "phone": "+9876543210"
        }
        
        updated_profile = update_profile(test_user, profile_data)
        
        assert updated_profile.display_name == "Updated Name"
        assert updated_profile.phone == "+9876543210"
        # Original data should remain
        assert updated_profile.first_name == "Test"

    def test_update_profile_new(self, db_session):
        """Test updating profile for user without existing profile"""
        from project_flask.utils.security import hash_password
        
        user = User(
            email="noprofile@example.com",
            password_hash=hash_password("TestPass123!")
        )
        db_session.add(user)
        db_session.commit()
        
        profile_data = {
            "display_name": "New Profile",
            "first_name": "New"
        }
        
        updated_profile = update_profile(user, profile_data)
        
        assert updated_profile.display_name == "New Profile"
        assert updated_profile.first_name == "New"

    def test_list_users_basic(self, db_session, test_user, admin_user):
        """Test basic user listing"""
        users, total = list_users()
        
        assert total >= 2  # At least test_user and admin_user
        user_emails = [u.email for u in users]
        assert test_user.email in user_emails
        assert admin_user.email in user_emails

    def test_list_users_pagination(self, db_session, user_role):
        """Test user listing with pagination"""
        # Create multiple users
        for i in range(5):
            create_user(f"user{i}@example.com", "TempPass123!", ["user"])
        
        users, total = list_users(page=1, per_page=2)
        
        assert len(users) == 2
        assert total >= 5

    def test_list_users_search(self, db_session, test_user):
        """Test user listing with search"""
        users, total = list_users(search="test@example.com")
        
        assert total >= 1
        assert test_user.email in [u.email for u in users]

    def test_list_users_filter_by_role(self, db_session, admin_user):
        """Test user listing filtered by role"""
        users, total = list_users(role="admin")
        
        assert total >= 1
        assert admin_user.email in [u.email for u in users]

    def test_list_users_filter_by_banned(self, db_session, banned_user):
        """Test user listing filtered by banned status"""
        users, total = list_users(is_banned=True)
        
        assert total >= 1
        assert banned_user.email in [u.email for u in users]

    def test_list_users_filter_by_active(self, db_session, inactive_user):
        """Test user listing filtered by active status"""
        users, total = list_users(is_active=False)
        
        assert total >= 1
        assert inactive_user.email in [u.email for u in users]

    def test_ban_user(self, db_session, test_user, admin_user):
        """Test banning a user"""
        banned_user = ban_user(
            admin_user.id,
            test_user,
            reason="Test ban reason"
        )
        
        assert banned_user.is_banned is True
        assert banned_user.banned_reason == "Test ban reason"
        assert banned_user.banned_by == admin_user.id
        assert banned_user.banned_at is not None

    def test_unban_user(self, db_session, banned_user):
        """Test unbanning a user"""
        unbanned_user = unban_user(banned_user)
        
        assert unbanned_user.is_banned is False
        assert unbanned_user.banned_reason is None
        assert unbanned_user.banned_by is None
        assert unbanned_user.banned_at is None


@pytest.mark.user
@pytest.mark.integration
class TestAdminUsersEndpoints:
    """Test admin user management endpoints"""

    def test_create_user_success(self, client, admin_auth_headers):
        """Test successful user creation by admin"""
        response = client.post('/api/admin/users', 
                              headers=admin_auth_headers,
                              json={
                                  'email': 'newuser@example.com',
                                  'temp_password': 'TempPass123!',
                                  'roles': ['user'],
                                  'profile': {
                                      'display_name': 'New User',
                                      'first_name': 'New',
                                      'last_name': 'User'
                                  }
                              })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == 'newuser@example.com'
        assert data['is_active'] is True
        assert 'user' in data['roles']

    def test_create_user_unauthorized(self, client):
        """Test user creation without authentication"""
        response = client.post('/api/admin/users', json={
            'email': 'newuser@example.com'
        })
        
        assert response.status_code == 401

    def test_create_user_forbidden(self, client, auth_headers):
        """Test user creation with non-admin user"""
        response = client.post('/api/admin/users',
                              headers=auth_headers,
                              json={
                                  'email': 'newuser@example.com'
                              })
        
        assert response.status_code == 403

    def test_create_user_invalid_data(self, client, admin_auth_headers):
        """Test user creation with invalid data"""
        response = client.post('/api/admin/users',
                              headers=admin_auth_headers,
                              json={
                                  'email': 'invalid-email'
                              })
        
        assert response.status_code == 422

    def test_list_roles(self, client, admin_auth_headers):
        """Test listing available roles"""
        response = client.get('/api/admin/users/roles',
                             headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert 'admin' in data
        assert 'user' in data

    def test_list_users(self, client, admin_auth_headers):
        """Test listing users as admin"""
        response = client.get('/api/admin/users',
                             headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data
        assert 'total' in data
        assert 'page' in data

    def test_list_users_with_search(self, client, admin_auth_headers):
        """Test listing users with search parameter"""
        response = client.get('/api/admin/users?search=admin',
                             headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data

    def test_list_users_with_role_filter(self, client, admin_auth_headers):
        """Test listing users with role filter"""
        response = client.get('/api/admin/users?role=admin',
                             headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data

    def test_get_user_by_id(self, client, admin_auth_headers, test_user):
        """Test getting specific user by ID"""
        response = client.get(f'/api/admin/users/{test_user.id}',
                             headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == test_user.id
        assert data['email'] == test_user.email

    def test_get_user_not_found(self, client, admin_auth_headers):
        """Test getting non-existent user"""
        response = client.get('/api/admin/users/non-existent-id',
                             headers=admin_auth_headers)
        
        assert response.status_code == 404

    def test_update_user(self, client, admin_auth_headers, test_user):
        """Test updating user as admin"""
        response = client.patch(f'/api/admin/users/{test_user.id}',
                               headers=admin_auth_headers,
                               json={
                                   'email': 'updated@example.com',
                                   'is_active': False,
                                   'roles': ['admin']
                               })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'updated@example.com'
        assert data['is_active'] is False
        assert 'admin' in data['roles']

    def test_ban_user(self, client, admin_auth_headers, test_user):
        """Test banning a user"""
        response = client.post(f'/api/admin/users/{test_user.id}/ban',
                              headers=admin_auth_headers,
                              json={
                                  'reason': 'Test ban'
                              })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['detail'] == 'user_banned'

    def test_unban_user(self, client, admin_auth_headers, banned_user):
        """Test unbanning a user"""
        response = client.post(f'/api/admin/users/{banned_user.id}/unban',
                              headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['detail'] == 'user_unbanned'


@pytest.mark.user
@pytest.mark.integration
class TestMeEndpoints:
    """Test /me endpoints for user self-management"""

    def test_get_me_success(self, client, auth_headers, test_user):
        """Test getting current user info"""
        response = client.get('/api/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == test_user.id
        assert data['email'] == test_user.email
        assert 'profile' in data

    def test_get_me_unauthorized(self, client):
        """Test getting current user info without authentication"""
        response = client.get('/api/me')
        
        assert response.status_code == 401

    def test_update_me_success(self, client, auth_headers):
        """Test updating current user profile"""
        response = client.patch('/api/me',
                               headers=auth_headers,
                               json={
                                   'display_name': 'Updated Name',
                                   'phone': '+1111111111',
                                   'timezone': 'UTC'
                               })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['display_name'] == 'Updated Name'
        assert data['phone'] == '+1111111111'
        assert data['timezone'] == 'UTC'

    def test_update_me_invalid_data(self, client, auth_headers):
        """Test updating current user profile with invalid data"""
        response = client.patch('/api/me',
                               headers=auth_headers,
                               json={
                                   'invalid_field': 'invalid_value'
                               })
        
        # Should still succeed but ignore invalid fields
        assert response.status_code == 200

    def test_update_me_unauthorized(self, client):
        """Test updating current user profile without authentication"""
        response = client.patch('/api/me', json={
            'display_name': 'Updated Name'
        })
        
        assert response.status_code == 401


@pytest.mark.user
@pytest.mark.integration 
class TestUserManagementEdgeCases:
    """Test edge cases and error conditions"""

    def test_create_user_duplicate_email(self, client, admin_auth_headers, test_user):
        """Test creating user with duplicate email"""
        response = client.post('/api/admin/users',
                              headers=admin_auth_headers,
                              json={
                                  'email': test_user.email,
                                  'temp_password': 'TempPass123!',
                                  'roles': ['user']
                              })
        
        # Should return error for duplicate email
        assert response.status_code >= 400

    def test_update_nonexistent_user(self, client, admin_auth_headers):
        """Test updating non-existent user"""
        response = client.patch('/api/admin/users/non-existent-id',
                               headers=admin_auth_headers,
                               json={'email': 'updated@example.com'})
        
        assert response.status_code == 404

    def test_ban_nonexistent_user(self, client, admin_auth_headers):
        """Test banning non-existent user"""
        response = client.post('/api/admin/users/non-existent-id/ban',
                              headers=admin_auth_headers,
                              json={'reason': 'Test'})
        
        assert response.status_code == 404

    def test_unban_nonexistent_user(self, client, admin_auth_headers):
        """Test unbanning non-existent user"""
        response = client.post('/api/admin/users/non-existent-id/unban',
                              headers=admin_auth_headers)
        
        assert response.status_code == 404

    def test_admin_operations_with_regular_user(self, client, auth_headers):
        """Test that regular users cannot perform admin operations"""
        endpoints = [
            '/api/admin/users',
            '/api/admin/users/roles',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint, headers=auth_headers)
            assert response.status_code == 403
