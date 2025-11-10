import os
import io
from flask import Blueprint, request, jsonify, current_app, send_file, abort
from werkzeug.datastructures import FileStorage
from PIL import Image

from ..schemas import CreateBuildingRequest, BuildingsListOut, BuildingOut
from ..utils.auth import login_required
from ..services.building_service import create_building, list_buildings, get_building_by_id, delete_building

buildings_bp = Blueprint("buildings", __name__, url_prefix="/buildings")

@buildings_bp.route("", methods=["POST"])
@login_required
def create_building_endpoint():
    """Create a new building with file uploads (accessible to all authenticated users)"""
    
    # Validate form data
    name = request.form.get('name')
    if not name or not name.strip():
        return jsonify({"detail": "Building name is required"}), 422
    
    # Validate name using schema
    try:
        body = CreateBuildingRequest.model_validate({"name": name.strip()})
    except Exception as e:
        return jsonify({"detail": "validation_error", "errors": str(e)}), 422
    
    # Check for uploaded files
    gml_file = request.files.get('gml_file')
    texture_file = request.files.get('texture_file')
    
    if not gml_file or gml_file.filename == '':
        return jsonify({"detail": "GML file is required"}), 422
    
    if not texture_file or texture_file.filename == '':
        return jsonify({"detail": "Texture file is required"}), 422
    
    # Validate file extensions
    if not gml_file.filename.lower().endswith('.gml'):
        return jsonify({"detail": "GML file must have .gml extension"}), 422
    
    if not texture_file.filename.lower().endswith(('.tif', '.tiff')):
        return jsonify({"detail": "Texture file must have .tif or .tiff extension"}), 422
    
    try:
        building = create_building(body.name, gml_file, texture_file)
        
        out = {
            "id": building.id,
            "name": building.name,
            "gml_file_path": building.gml_file_path,
            "texture_file_path": building.texture_file_path,
            "xml_data": building.xml_data,
            "created_at": building.created_at.isoformat() if building.created_at else None,
        }
        return jsonify(BuildingOut.model_validate(out).model_dump()), 201
        
    except Exception as e:
        return jsonify({"detail": f"Failed to create building: {str(e)}"}), 500

@buildings_bp.route("", methods=["GET"])
@login_required
def list_buildings_endpoint():
    """List buildings with pagination (accessible to all authenticated users)"""
    
    # Query parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", current_app.config.get("DEFAULT_PER_PAGE", 25)))
    per_page = min(per_page, current_app.config.get("MAX_PER_PAGE", 200))
    search = request.args.get("search")
    sort = request.args.get("sort", "created_at_desc")
    
    try:
        buildings, total = list_buildings(page=page, per_page=per_page, search=search, sort=sort)
        
        out_items = []
        for building in buildings:
            out_items.append({
                "id": building.id,
                "name": building.name,
                "gml_file_path": building.gml_file_path,
                "texture_file_path": building.texture_file_path,
                "xml_data": building.xml_data,
                "created_at": building.created_at.isoformat() if building.created_at else None,
            })
        
        # Compute total pages for frontend pagination helpers
        total_pages = (total + per_page - 1) // per_page if per_page else 0
        
        resp = {
            "items": out_items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
        }
        
        return jsonify(BuildingsListOut.model_validate(resp).model_dump()), 200
        
    except Exception as e:
        return jsonify({"detail": f"Failed to list buildings: {str(e)}"}), 500

@buildings_bp.route("/<building_id>", methods=["GET"])
@login_required
def get_building_endpoint(building_id):
    """Get a single building by ID (accessible to all authenticated users)"""
    
    building = get_building_by_id(building_id)
    if not building:
        return jsonify({"detail": "Building not found"}), 404
    
    out = {
        "id": building.id,
        "name": building.name,
        "gml_file_path": building.gml_file_path,
        "texture_file_path": building.texture_file_path,
        "xml_data": building.xml_data,
        "created_at": building.created_at.isoformat() if building.created_at else None,
    }
    
    return jsonify(BuildingOut.model_validate(out).model_dump()), 200

@buildings_bp.route("/<building_id>", methods=["DELETE"])
@login_required
def delete_building_endpoint(building_id):
    """Delete a building (accessible to all authenticated users)"""
    
    building = get_building_by_id(building_id)
    if not building:
        return jsonify({"detail": "Building not found"}), 404
    
    try:
        success = delete_building(building_id)
        if success:
            return jsonify({"detail": "Building deleted successfully", "building_id": building_id}), 200
        else:
            return jsonify({"detail": "Failed to delete building"}), 500
    except Exception as e:
        return jsonify({"detail": f"Failed to delete building: {str(e)}"}), 500

@buildings_bp.route("/<building_id>/texture", methods=["GET"])
@login_required
def serve_texture_file(building_id):
    """Serve the texture file for a building converted to PNG format (accessible to all authenticated users)"""
    
    building = get_building_by_id(building_id)
    if not building:
        return jsonify({"detail": "Building not found"}), 404
    
    texture_path = building.texture_file_path
    if not os.path.exists(texture_path):
        return jsonify({"detail": "Texture file not found"}), 404
    
    try:
        # Convert TIF to PNG for web browser compatibility
        with Image.open(texture_path) as img:
            # Convert to RGB if necessary (for transparency compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGBA')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create in-memory PNG
            png_io = io.BytesIO()
            img.save(png_io, format='PNG')
            png_io.seek(0)
            
            return send_file(png_io, mimetype='image/png', as_attachment=False)
            
    except Exception as e:
        return jsonify({"detail": f"Failed to process texture file: {str(e)}"}), 500
