# Building Module Tutorial: Step-by-Step Implementation

This tutorial explains how to add a complete building management module to a Flask project, including file uploads, image processing, and full CRUD functionality.

## Table of Contents

1. [Overview](#overview)
2. [Step 1: Database Model](#step-1-database-model)
3. [Step 2: Validation Schemas](#step-2-validation-schemas)
4. [Step 3: Business Logic Service](#step-3-business-logic-service)
5. [Step 4: API Endpoints](#step-4-api-endpoints)
6. [Step 5: Frontend Template](#step-5-frontend-template)
7. [Step 6: API Client](#step-6-api-client)
8. [Step 7: Frontend JavaScript](#step-7-frontend-javascript)
9. [Step 8: Navigation Integration](#step-8-navigation-integration)
10. [Step 9: Image Processing](#step-9-image-processing)
11. [Step 10: Testing](#step-10-testing)
12. [Best Practices](#best-practices)

## Overview

We're building a module that allows users to:
- Upload buildings with GML files (containing XML data) and TIF texture files
- View building lists with pagination and search
- Display texture images (converting TIF to PNG for web compatibility)
- Manage buildings with full CRUD operations

**Architecture Pattern:** We follow a layered architecture:
- **Models** (Database layer)
- **Schemas** (Validation layer) 
- **Services** (Business logic layer)
- **Blueprints** (API layer)
- **Templates & JavaScript** (Presentation layer)

## Step 1: Database Model

**File:** `project_flask/models.py`

First, we create the database model to store building information.

```python
class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(255), nullable=False)
    gml_file_path = db.Column(db.Text, nullable=False)
    texture_file_path = db.Column(db.Text, nullable=False)
    xml_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
```

**Key Design Decisions:**
- `id`: UUID string for unique identification
- `name`: Building name (user-friendly identifier)
- `gml_file_path` & `texture_file_path`: Store file system paths
- `xml_data`: Extracted XML content from GML file for easy access
- `created_at`: Timestamp for sorting and auditing

**Why This Design:**
- Separates file storage (paths) from content (XML data)
- Enables efficient searching without file system access
- Follows existing project patterns (UUID, timestamps)

## Step 2: Validation Schemas

**File:** `project_flask/schemas.py`

We define Pydantic schemas for data validation and serialization.

```python
class BuildingOut(BaseModel):
    id: str
    name: str
    gml_file_path: str
    texture_file_path: str
    xml_data: str
    created_at: str

class CreateBuildingRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class BuildingsListOut(BaseModel):
    items: List[BuildingOut]
    total: int
    page: int
    per_page: int
    total_pages: Optional[int] = None
```

**Schema Purposes:**
- `BuildingOut`: Serializes building data for API responses
- `CreateBuildingRequest`: Validates building creation input
- `BuildingsListOut`: Structures paginated list responses

**Validation Benefits:**
- Type safety
- Automatic documentation
- Input sanitization
- Consistent API responses

## Step 3: Business Logic Service

**File:** `project_flask/services/building_service.py`

The service layer handles business logic and file operations.

```python
def create_building(name: str, gml_file: FileStorage, texture_file: FileStorage) -> Building:
    """Create a new building with uploaded GML and texture files"""
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Save files with secure names
    gml_filename = secure_filename(gml_file.filename)
    gml_path = os.path.join(uploads_dir, f"gml_{gml_filename}")
    gml_file.save(gml_path)
    
    texture_filename = secure_filename(texture_file.filename)
    texture_path = os.path.join(uploads_dir, f"texture_{texture_filename}")
    texture_file.save(texture_path)
    
    # Extract XML data from GML file
    xml_data = extract_xml_from_gml(gml_path)
    
    # Create database record
    building = Building(
        name=name,
        gml_file_path=gml_path,
        texture_file_path=texture_path,
        xml_data=xml_data
    )
    
    db.session.add(building)
    db.session.commit()
    
    return building
```

**Key Service Functions:**
- `create_building()`: Handles file upload and database creation
- `list_buildings()`: Provides paginated building lists with search
- `get_building_by_id()`: Retrieves single building
- `delete_building()`: Removes building and associated files

**Service Layer Benefits:**
- Separates business logic from API layer
- Reusable across different interfaces
- Easier to test
- Consistent error handling

## Step 4: API Endpoints

**File:** `project_flask/blueprints/buildings.py`

We create RESTful API endpoints following the project's patterns.

```python
@buildings_bp.route("", methods=["POST"])
@login_required
def create_building_endpoint():
    """Create a new building with file uploads"""
    
    # Validate form data
    name = request.form.get('name')
    if not name or not name.strip():
        return jsonify({"detail": "Building name is required"}), 422
    
    # Validate files
    gml_file = request.files.get('gml_file')
    texture_file = request.files.get('texture_file')
    
    # File extension validation
    if not gml_file.filename.lower().endswith('.gml'):
        return jsonify({"detail": "GML file must have .gml extension"}), 422
    
    if not texture_file.filename.lower().endswith(('.tif', '.tiff')):
        return jsonify({"detail": "Texture file must have .tif or .tiff extension"}), 422
    
    try:
        building = create_building(name.strip(), gml_file, texture_file)
        return jsonify(BuildingOut.model_validate(building).model_dump()), 201
    except Exception as e:
        return jsonify({"detail": f"Failed to create building: {str(e)}"}), 500
```

**API Design Principles:**
- RESTful URLs (`GET /buildings`, `POST /buildings`, etc.)
- Consistent error responses
- Proper HTTP status codes
- Authentication required (`@login_required`)
- File validation before processing

**Endpoint Structure:**
- `POST /buildings` - Create building
- `GET /buildings` - List buildings (with pagination)
- `GET /buildings/<id>` - Get single building
- `DELETE /buildings/<id>` - Delete building
- `GET /buildings/<id>/texture` - Serve texture image

## Step 5: Frontend Template

**File:** `project_flask/templates/buildings.html`

We create a responsive HTML template with Bootstrap styling.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Buildings</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div id="navbar"></div>
  <main class="container py-4">
    <!-- Page Header -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1 class="h4">Buildings</h1>
      <button id="createBuildingBtn" class="btn btn-sm btn-primary">Upload Building</button>
    </div>

    <!-- Search/Filter Section -->
    <div id="filters" class="card mb-3 p-3">
      <form id="filtersForm" class="row g-2 align-items-end">
        <div class="col-md-6">
          <label class="form-label">Search</label>
          <input name="search" class="form-control" placeholder="Search building name">
        </div>
        <!-- Sort options -->
      </form>
    </div>

    <!-- Buildings Table -->
    <div class="table-responsive">
      <table class="table table-sm table-hover">
        <thead class="table-light sticky-top">
          <tr>
            <th>Name</th>
            <th>GML File</th>
            <th>Texture File</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="buildingsTbody">
          <!-- Populated by JavaScript -->
        </tbody>
      </table>
    </div>
  </main>
</body>
</html>
```

**Template Structure:**
- **Navigation**: Integrated navbar
- **Filters**: Search and sort controls
- **Table**: Responsive data display
- **Modals**: Create and view building details
- **JavaScript Integration**: ES6 modules for functionality

## Step 6: API Client

**File:** `project_flask/static/assets/js/api/buildingsApi.js`

We create a JavaScript API client following the project's patterns.

```javascript
import { apiFetch } from '../auth/fetchClient.js';

export function listBuildings(params) { 
  const qs = new URLSearchParams(params || {}).toString();
  return apiFetch('/buildings?' + qs, { method: 'GET' });
}

export function createBuilding(formData) { 
  // Special handling for file uploads
  const getAccessToken = () => {
    try {
      return sessionStorage.getItem('pf_access') || localStorage.getItem('access_token');
    } catch (e) {
      return null;
    }
  };

  const accessToken = getAccessToken();
  const headers = {};
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`;
  }

  return fetch('/api/buildings', {
    method: 'POST',
    headers: headers,
    body: formData // FormData passed as-is for file uploads
  }).then(response => {
    if (!response.ok) {
      return response.json().then(err => Promise.reject(err));
    }
    return response.json();
  });
}
```

**API Client Features:**
- Consistent interface with other API clients
- Authentication handling
- Special FormData handling for file uploads
- Error handling and response parsing

**Why Separate File Upload Logic:**
- FormData requires different handling than JSON
- Browser must set Content-Type header automatically
- Authentication still required for security

## Step 7: Frontend JavaScript

**File:** `project_flask/static/assets/js/pages/buildings.js`

The main JavaScript file handles all frontend interactions.

```javascript
// Load buildings with pagination
async function load(page = 1) {
  const perPage = parseInt(document.getElementById('perPageSelect')?.value || 10);
  const params = { page, per_page: perPage };
  
  // Gather search/filter parameters
  const filtersForm = document.getElementById('filtersForm');
  if (filtersForm) {
    const fd = new FormData(filtersForm);
    const search = (fd.get('search') || '').trim();
    if (search) params.search = search;
  }

  try {
    const data = await listBuildings(params);
    renderBuildingsTable(data);
    renderPagination(data);
  } catch (e) {
    showError('Failed to load buildings');
  }
}

// Handle building creation
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(form);
  
  // Client-side validation
  const name = (formData.get('name') || '').trim();
  if (!name) {
    showValidationError('name', 'Building name is required');
    return;
  }

  try {
    await createBuilding(formData);
    showSuccess('Building uploaded successfully');
    modal.hide();
    load(currentPage); // Refresh list
  } catch (err) {
    showError(err.detail || 'Failed to upload building');
  }
});
```

**JavaScript Architecture:**
- **Module Structure**: ES6 imports for clean dependencies
- **Event Handling**: Proper event delegation and cleanup
- **State Management**: Simple state tracking (currentPage)
- **Error Handling**: User-friendly error messages
- **Validation**: Client and server-side validation

## Step 8: Navigation Integration

**File:** `project_flask/static/assets/js/components/navbar.js`

We add the buildings link to the navigation component.

```javascript
export async function renderNavbar(containerId='navbar'){
  const el = document.getElementById(containerId);
  try{
    const me = await apiFetch('/me', { method: 'GET' });
    const roles = me.roles||[];
    const email = me.email;
    el.innerHTML = `
<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
  <div class="container">
    <a class="navbar-brand" href="/"><strong>ProjectFlask</strong></a>
    <div class="collapse navbar-collapse" id="navMain">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item"><a class="nav-link" href="/buildings.html">Buildings</a></li>
        ${roles.includes('admin') ? '<li class="nav-item"><a class="nav-link" href="/admin/users.html">Users</a></li>' : ''}
        <li class="nav-item"><a class="nav-link" href="/me.html">My Profile</a></li>
      </ul>
    </div>
  </div>
</nav>`;
  }catch(e){
    el.innerHTML = '';
  }
}
```

**Navigation Integration:**
- Available to all authenticated users (not admin-only)
- Consistent with existing navigation patterns
- Dynamic rendering based on user permissions

## Step 9: Image Processing

**Key Challenge:** TIF files aren't supported by web browsers.

**Solution:** Server-side image conversion using Pillow.

```python
# Add to requirements.txt
Pillow>=10.0

# Texture serving endpoint
@buildings_bp.route("/<building_id>/texture", methods=["GET"])
@login_required
def serve_texture_file(building_id):
    """Serve texture file converted to PNG format"""
    
    building = get_building_by_id(building_id)
    if not building:
        return jsonify({"detail": "Building not found"}), 404
    
    try:
        # Convert TIF to PNG for web browser compatibility
        with Image.open(building.texture_file_path) as img:
            # Handle different image modes
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
```

**Image Processing Benefits:**
- **Browser Compatibility**: PNG works in all browsers
- **Memory Efficient**: No temporary files created
- **Format Flexibility**: Handles various TIF modes
- **Quality Preservation**: No loss during conversion

## Step 10: Testing

### Manual Testing Steps:

1. **Authentication Test**
   ```bash
   curl -X GET http://localhost:5000/api/buildings
   # Should return 401 "Missing auth token"
   ```

2. **Page Load Test**
   ```bash
   curl -X GET http://localhost:5000/buildings.html
   # Should return the HTML template
   ```

3. **File Upload Test**
   - Login to the application
   - Navigate to Buildings page
   - Click "Upload Building"
   - Fill form with name, select GML and TIF files
   - Submit and verify success

4. **Image Display Test**
   - Click "View" on any building
   - Verify texture image displays properly
   - Check browser console for any errors

### Automated Testing Suggestions:

```python
# Test building creation
def test_create_building():
    with app.test_client() as client:
        # Login first
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password'
        })
        
        # Upload building
        response = client.post('/api/buildings', data={
            'name': 'Test Building',
            'gml_file': (io.BytesIO(b'<gml>test</gml>'), 'test.gml'),
            'texture_file': (io.BytesIO(b'dummy_tif'), 'test.tif')
        })
        
        assert response.status_code == 201
```

## Best Practices

### 1. Security
- **File Validation**: Always validate file extensions and content
- **Authentication**: Require authentication for all operations
- **Path Security**: Use `secure_filename()` to prevent path traversal
- **Input Sanitization**: Validate all user inputs

### 2. Performance
- **Pagination**: Implement server-side pagination for large datasets
- **Image Processing**: Use in-memory processing to avoid disk I/O
- **Database Indexes**: Add indexes on frequently searched columns
- **File Storage**: Consider cloud storage for production

### 3. User Experience
- **Loading States**: Show progress during file uploads
- **Error Handling**: Provide clear, actionable error messages
- **Responsive Design**: Ensure mobile compatibility
- **Accessibility**: Use semantic HTML and proper ARIA labels

### 4. Maintainability
- **Separation of Concerns**: Keep layers distinct (model, service, API, UI)
- **Consistent Patterns**: Follow existing project conventions
- **Documentation**: Document complex business logic
- **Error Logging**: Log errors for debugging

### 5. Scalability
- **File Storage**: Plan for file storage growth
- **Database Performance**: Monitor query performance
- **Caching**: Consider caching for frequently accessed images
- **Async Processing**: Consider background jobs for large file processing

## Summary

This tutorial covered building a complete module with:

- ✅ Database modeling with proper relationships
- ✅ Input validation and error handling  
- ✅ File upload and processing
- ✅ RESTful API design
- ✅ Responsive frontend with search/pagination
- ✅ Image processing for web compatibility
- ✅ Authentication and authorization
- ✅ Integration with existing system patterns

The modular approach ensures the building functionality integrates seamlessly with the existing Flask application while maintaining code quality and following established patterns.
