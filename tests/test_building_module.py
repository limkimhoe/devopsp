"""
Building module tests
"""
import pytest
import os
import tempfile
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock, mock_open
from werkzeug.datastructures import FileStorage
from io import BytesIO

from project_flask.models import Building
from project_flask.services.building_service import (
    create_building, get_building_by_id, list_buildings, delete_building, extract_xml_from_gml
)


@pytest.mark.building
@pytest.mark.unit
class TestBuildingService:
    """Test building service functions"""

    def test_extract_xml_from_gml_success(self):
        """Test successful XML extraction from GML file"""
        gml_content = '<?xml version="1.0"?><gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml"><gml:featureMember><building>Test Building</building></gml:featureMember></gml:FeatureCollection>'
        
        with patch('builtins.open', mock_open(read_data=gml_content)):
            result = extract_xml_from_gml('/test/path/file.gml')
            assert gml_content in result

    def test_extract_xml_from_gml_invalid_xml(self):
        """Test XML extraction with invalid XML"""
        invalid_content = '<invalid>xml without closing tag'
        
        with patch('builtins.open', mock_open(read_data=invalid_content)):
            result = extract_xml_from_gml('/test/path/file.gml')
            assert '<error>' in result
            assert 'Failed to parse GML file' in result

    def test_extract_xml_from_gml_file_error(self):
        """Test XML extraction with file read error"""
        with patch('builtins.open', side_effect=IOError("File not found")):
            result = extract_xml_from_gml('/test/path/file.gml')
            assert '<error>' in result
            assert 'File not found' in result

    def test_get_building_by_id_exists(self, db_session, test_building):
        """Test getting existing building by ID"""
        found_building = get_building_by_id(test_building.id)
        assert found_building is not None
        assert found_building.id == test_building.id
        assert found_building.name == test_building.name

    def test_get_building_by_id_not_exists(self, db_session):
        """Test getting non-existent building by ID"""
        found_building = get_building_by_id("non-existent-id")
        assert found_building is None

    @patch('os.makedirs')
    @patch('os.getcwd')
    def test_create_building_success(self, mock_getcwd, mock_makedirs, db_session):
        """Test successful building creation"""
        # Mock working directory
        mock_getcwd.return_value = '/test'
        
        # Mock files
        gml_content = b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>'
        texture_content = b'fake tiff content'
        
        gml_file = MagicMock(spec=FileStorage)
        gml_file.filename = 'test.gml'
        gml_file.save = MagicMock()
        
        texture_file = MagicMock(spec=FileStorage)
        texture_file.filename = 'test.tif'
        texture_file.save = MagicMock()
        
        with patch('project_flask.services.building_service.extract_xml_from_gml', return_value='<test>xml</test>'):
            building = create_building('Test Building', gml_file, texture_file)
            
            assert building.name == 'Test Building'
            assert 'gml_test.gml' in building.gml_file_path
            assert 'texture_test.tif' in building.texture_file_path
            assert building.xml_data == '<test>xml</test>'
            
            # Verify files were saved
            gml_file.save.assert_called_once()
            texture_file.save.assert_called_once()
            mock_makedirs.assert_called_once()

    def test_list_buildings_basic(self, db_session, test_building):
        """Test basic building listing"""
        buildings, total = list_buildings()
        
        assert total >= 1
        building_names = [b.name for b in buildings]
        assert test_building.name in building_names

    def test_list_buildings_pagination(self, db_session):
        """Test building listing with pagination"""
        # Create multiple buildings
        for i in range(5):
            building = Building(
                name=f'Test Building {i}',
                gml_file_path=f'/test/gml_{i}.gml',
                texture_file_path=f'/test/texture_{i}.tif',
                xml_data=f'<test>building_{i}</test>'
            )
            db_session.add(building)
        db_session.commit()
        
        buildings, total = list_buildings(page=1, per_page=2)
        
        assert len(buildings) == 2
        assert total >= 5

    def test_list_buildings_search(self, db_session, test_building):
        """Test building listing with search"""
        buildings, total = list_buildings(search="Test Building")
        
        assert total >= 1
        assert test_building.name in [b.name for b in buildings]

    def test_list_buildings_search_no_results(self, db_session):
        """Test building listing with search that returns no results"""
        buildings, total = list_buildings(search="NonExistentBuilding")
        
        assert total == 0
        assert len(buildings) == 0

    def test_list_buildings_sort_name_asc(self, db_session):
        """Test building listing sorted by name ascending"""
        # Create buildings with different names
        building_a = Building(
            name='A Building',
            gml_file_path='/test/a.gml',
            texture_file_path='/test/a.tif',
            xml_data='<test>a</test>'
        )
        building_z = Building(
            name='Z Building',
            gml_file_path='/test/z.gml',
            texture_file_path='/test/z.tif',
            xml_data='<test>z</test>'
        )
        db_session.add(building_a)
        db_session.add(building_z)
        db_session.commit()
        
        buildings, total = list_buildings(sort="name_asc")
        
        assert buildings[0].name == 'A Building'

    def test_list_buildings_sort_name_desc(self, db_session):
        """Test building listing sorted by name descending"""
        # Create buildings with different names
        building_a = Building(
            name='A Building',
            gml_file_path='/test/a.gml',
            texture_file_path='/test/a.tif',
            xml_data='<test>a</test>'
        )
        building_z = Building(
            name='Z Building',
            gml_file_path='/test/z.gml',
            texture_file_path='/test/z.tif',
            xml_data='<test>z</test>'
        )
        db_session.add(building_a)
        db_session.add(building_z)
        db_session.commit()
        
        buildings, total = list_buildings(sort="name_desc")
        
        assert buildings[0].name == 'Z Building'

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_building_success(self, mock_remove, mock_exists, db_session, test_building):
        """Test successful building deletion"""
        mock_exists.return_value = True
        
        result = delete_building(test_building.id)
        
        assert result is True
        # Verify files were removed
        assert mock_remove.call_count == 2  # GML and texture files
        
        # Verify building was deleted from database
        deleted_building = get_building_by_id(test_building.id)
        assert deleted_building is None

    def test_delete_building_not_exists(self, db_session):
        """Test deleting non-existent building"""
        result = delete_building("non-existent-id")
        assert result is False

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_building_file_deletion_fails(self, mock_remove, mock_exists, db_session, test_building):
        """Test building deletion when file deletion fails"""
        mock_exists.return_value = True
        mock_remove.side_effect = OSError("Permission denied")
        
        # Should still succeed even if file deletion fails
        result = delete_building(test_building.id)
        assert result is True
        
        # Building should still be deleted from database
        deleted_building = get_building_by_id(test_building.id)
        assert deleted_building is None


@pytest.mark.building
@pytest.mark.integration
class TestBuildingEndpoints:
    """Test building management endpoints"""

    @patch('os.makedirs')
    @patch('os.getcwd')
    def test_create_building_success(self, mock_getcwd, mock_makedirs, client, auth_headers):
        """Test successful building creation via endpoint"""
        mock_getcwd.return_value = '/test'
        
        # Create mock file data
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake tiff content')
        
        with patch('project_flask.services.building_service.extract_xml_from_gml', return_value='<test>xml</test>'):
            response = client.post('/api/buildings',
                                 headers=auth_headers,
                                 data={
                                     'name': 'Test Building API',
                                     'gml_file': (gml_data, 'test.gml'),
                                     'texture_file': (texture_data, 'test.tif')
                                 },
                                 content_type='multipart/form-data')
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Test Building API'
        assert data['xml_data'] == '<test>xml</test>'

    def test_create_building_unauthorized(self, client):
        """Test building creation without authentication"""
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake tiff content')
        
        response = client.post('/api/buildings',
                             data={
                                 'name': 'Test Building',
                                 'gml_file': (gml_data, 'test.gml'),
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 401

    def test_create_building_missing_name(self, client, auth_headers):
        """Test building creation without name"""
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake tiff content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'gml_file': (gml_data, 'test.gml'),
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'Building name is required' in data['detail']

    def test_create_building_missing_gml_file(self, client, auth_headers):
        """Test building creation without GML file"""
        texture_data = BytesIO(b'fake tiff content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': 'Test Building',
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'GML file is required' in data['detail']

    def test_create_building_missing_texture_file(self, client, auth_headers):
        """Test building creation without texture file"""
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': 'Test Building',
                                 'gml_file': (gml_data, 'test.gml')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'Texture file is required' in data['detail']

    def test_create_building_invalid_gml_extension(self, client, auth_headers):
        """Test building creation with invalid GML file extension"""
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake tiff content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': 'Test Building',
                                 'gml_file': (gml_data, 'test.xml'),  # Wrong extension
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'GML file must have .gml extension' in data['detail']

    def test_create_building_invalid_texture_extension(self, client, auth_headers):
        """Test building creation with invalid texture file extension"""
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake image content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': 'Test Building',
                                 'gml_file': (gml_data, 'test.gml'),
                                 'texture_file': (texture_data, 'test.jpg')  # Wrong extension
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'Texture file must have .tif or .tiff extension' in data['detail']

    def test_list_buildings(self, client, auth_headers):
        """Test listing buildings"""
        response = client.get('/api/buildings', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data
        assert 'total' in data
        assert 'page' in data
        assert 'per_page' in data

    def test_list_buildings_unauthorized(self, client):
        """Test listing buildings without authentication"""
        response = client.get('/api/buildings')
        
        assert response.status_code == 401

    def test_list_buildings_with_search(self, client, auth_headers):
        """Test listing buildings with search parameter"""
        response = client.get('/api/buildings?search=Test', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data

    def test_list_buildings_with_pagination(self, client, auth_headers):
        """Test listing buildings with pagination parameters"""
        response = client.get('/api/buildings?page=1&per_page=5', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['page'] == 1
        assert data['per_page'] == 5

    def test_list_buildings_with_sort(self, client, auth_headers):
        """Test listing buildings with sort parameter"""
        response = client.get('/api/buildings?sort=name_asc', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data

    def test_get_building_by_id(self, client, auth_headers, test_building):
        """Test getting specific building by ID"""
        response = client.get(f'/api/buildings/{test_building.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == test_building.id
        assert data['name'] == test_building.name

    def test_get_building_not_found(self, client, auth_headers):
        """Test getting non-existent building"""
        response = client.get('/api/buildings/non-existent-id', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Building not found' in data['detail']

    def test_get_building_unauthorized(self, client, test_building):
        """Test getting building without authentication"""
        response = client.get(f'/api/buildings/{test_building.id}')
        
        assert response.status_code == 401

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_building(self, mock_remove, mock_exists, client, auth_headers, test_building):
        """Test deleting a building"""
        mock_exists.return_value = True
        
        response = client.delete(f'/api/buildings/{test_building.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Building deleted successfully' in data['detail']

    def test_delete_building_not_found(self, client, auth_headers):
        """Test deleting non-existent building"""
        response = client.delete('/api/buildings/non-existent-id', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Building not found' in data['detail']

    def test_delete_building_unauthorized(self, client, test_building):
        """Test deleting building without authentication"""
        response = client.delete(f'/api/buildings/{test_building.id}')
        
        assert response.status_code == 401

    @patch('os.path.exists')
    @patch('PIL.Image.open')
    def test_serve_texture_file(self, mock_image_open, mock_exists, client, auth_headers, test_building):
        """Test serving texture file"""
        mock_exists.return_value = True
        
        # Mock PIL Image
        mock_img = MagicMock()
        mock_img.mode = 'RGB'
        mock_img.save = MagicMock()
        mock_image_open.return_value.__enter__.return_value = mock_img
        
        response = client.get(f'/api/buildings/{test_building.id}/texture', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.mimetype == 'image/png'

    def test_serve_texture_file_building_not_found(self, client, auth_headers):
        """Test serving texture file for non-existent building"""
        response = client.get('/api/buildings/non-existent-id/texture', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Building not found' in data['detail']

    @patch('os.path.exists')
    def test_serve_texture_file_not_found(self, mock_exists, client, auth_headers, test_building):
        """Test serving texture file when file doesn't exist"""
        mock_exists.return_value = False
        
        response = client.get(f'/api/buildings/{test_building.id}/texture', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Texture file not found' in data['detail']

    def test_serve_texture_file_unauthorized(self, client, test_building):
        """Test serving texture file without authentication"""
        response = client.get(f'/api/buildings/{test_building.id}/texture')
        
        assert response.status_code == 401


@pytest.mark.building
@pytest.mark.integration
class TestBuildingModuleEdgeCases:
    """Test edge cases and error conditions for building module"""

    @patch('project_flask.services.building_service.create_building')
    def test_create_building_service_error(self, mock_create, client, auth_headers):
        """Test building creation when service raises exception"""
        mock_create.side_effect = Exception("Database error")
        
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake tiff content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': 'Test Building',
                                 'gml_file': (gml_data, 'test.gml'),
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Failed to create building' in data['detail']

    @patch('project_flask.services.building_service.list_buildings')
    def test_list_buildings_service_error(self, mock_list, client, auth_headers):
        """Test building listing when service raises exception"""
        mock_list.side_effect = Exception("Database error")
        
        response = client.get('/api/buildings', headers=auth_headers)
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Failed to list buildings' in data['detail']

    @patch('project_flask.services.building_service.delete_building')
    def test_delete_building_service_error(self, mock_delete, client, auth_headers, test_building):
        """Test building deletion when service raises exception"""
        mock_delete.side_effect = Exception("Filesystem error")
        
        response = client.delete(f'/api/buildings/{test_building.id}', headers=auth_headers)
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Failed to delete building' in data['detail']

    @patch('os.path.exists')
    @patch('PIL.Image.open')
    def test_serve_texture_file_processing_error(self, mock_image_open, mock_exists, client, auth_headers, test_building):
        """Test serving texture file when image processing fails"""
        mock_exists.return_value = True
        mock_image_open.side_effect = Exception("Image processing error")
        
        response = client.get(f'/api/buildings/{test_building.id}/texture', headers=auth_headers)
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Failed to process texture file' in data['detail']

    def test_create_building_empty_name(self, client, auth_headers):
        """Test building creation with empty name"""
        gml_data = BytesIO(b'<?xml version="1.0"?><gml:FeatureCollection></gml:FeatureCollection>')
        texture_data = BytesIO(b'fake tiff content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': '   ',  # Empty/whitespace name
                                 'gml_file': (gml_data, 'test.gml'),
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'Building name is required' in data['detail']

    def test_create_building_empty_filename(self, client, auth_headers):
        """Test building creation with empty filenames"""
        gml_data = BytesIO(b'content')
        texture_data = BytesIO(b'content')
        
        response = client.post('/api/buildings',
                             headers=auth_headers,
                             data={
                                 'name': 'Test Building',
                                 'gml_file': (gml_data, ''),  # Empty filename
                                 'texture_file': (texture_data, 'test.tif')
                             },
                             content_type='multipart/form-data')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'GML file is required' in data['detail']
