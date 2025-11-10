import os
import xml.etree.ElementTree as ET
from typing import Optional, List, Tuple
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from sqlalchemy import func

from ..models import Building
from ..extensions import db

def create_building(name: str, gml_file: FileStorage, texture_file: FileStorage) -> Building:
    """Create a new building with uploaded GML and texture files"""
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Save GML file
    gml_filename = secure_filename(gml_file.filename)
    gml_path = os.path.join(uploads_dir, f"gml_{gml_filename}")
    gml_file.save(gml_path)
    
    # Save texture file
    texture_filename = secure_filename(texture_file.filename)
    texture_path = os.path.join(uploads_dir, f"texture_{texture_filename}")
    texture_file.save(texture_path)
    
    # Extract XML data from GML file
    xml_data = extract_xml_from_gml(gml_path)
    
    # Create building record
    building = Building(
        name=name,
        gml_file_path=gml_path,
        texture_file_path=texture_path,
        xml_data=xml_data
    )
    
    db.session.add(building)
    db.session.commit()
    
    return building

def extract_xml_from_gml(gml_file_path: str) -> str:
    """Extract XML data from GML file"""
    try:
        with open(gml_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Parse the XML to validate it and extract meaningful data
            root = ET.fromstring(content)
            # Return the XML content as string
            return content
    except Exception as e:
        # If parsing fails, return a simple error message in XML format
        return f"<error>Failed to parse GML file: {str(e)}</error>"

def get_building_by_id(building_id: str) -> Optional[Building]:
    """Get a building by its ID"""
    return Building.query.get(building_id)

def list_buildings(page: int = 1, per_page: int = 25, search: Optional[str] = None, sort: str = "created_at_desc") -> Tuple[List[Building], int]:
    """List buildings with pagination and optional search"""
    q = Building.query
    
    if search:
        search_pattern = f"%{search}%"
        q = q.filter(Building.name.ilike(search_pattern))
    
    if sort == "created_at_asc":
        q = q.order_by(Building.created_at.asc(), Building.id.asc())
    elif sort == "name_asc":
        q = q.order_by(Building.name.asc(), Building.id.asc())
    elif sort == "name_desc":
        q = q.order_by(Building.name.desc(), Building.id.desc())
    else:  # default: created_at_desc
        q = q.order_by(Building.created_at.desc(), Building.id.desc())
    
    # Get total count
    total = q.order_by(None).with_entities(func.count(Building.id)).scalar() or 0
    
    # Get paginated items
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    
    return items, total

def delete_building(building_id: str) -> bool:
    """Delete a building and its associated files"""
    building = get_building_by_id(building_id)
    if not building:
        return False
    
    # Delete files from filesystem
    try:
        if os.path.exists(building.gml_file_path):
            os.remove(building.gml_file_path)
        if os.path.exists(building.texture_file_path):
            os.remove(building.texture_file_path)
    except Exception:
        pass  # Continue even if file deletion fails
    
    # Delete from database
    db.session.delete(building)
    db.session.commit()
    
    return True
