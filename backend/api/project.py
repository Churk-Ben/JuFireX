from flask import Blueprint, request, jsonify, session, current_app
from backend.data.repositories.project_repo import ProjectRepository
from backend.core.security import require_login, require_role
from backend.config import ROLE_ADMIN

project_bp = Blueprint("project", __name__)
repo = ProjectRepository()

@project_bp.route("/", methods=["GET"])
def list_projects():
    projects = repo.list_items()
    return jsonify(projects)

@project_bp.route("/featured", methods=["GET"])
def list_featured_projects():
    projects = repo.get_featured_projects()
    return jsonify(projects)

@project_bp.route("/<project_id>", methods=["GET"])
def get_project(project_id):
    metadata = repo.get_metadata(project_id)
    if not metadata:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(metadata)

@project_bp.route("/", methods=["POST"])
@require_login
def create_project():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Generate ID (simple slug or uuid, here using title slug or timestamp for simplicity, 
    # but strictly file repo usually needs a unique folder name)
    import uuid
    project_id = str(uuid.uuid4())
    
    metadata = {
        "title": title,
        "description": data.get("description", ""),
        "github_url": data.get("github_url", ""),
        "demo_url": data.get("demo_url", ""),
        "image_url": data.get("image_url", ""),
        "is_featured": data.get("is_featured", False),
        "author_id": session.get("user_id"),
        "created_at": str(uuid.uuid1().time) # Placeholder timestamp
    }
    
    if repo.create_item(project_id, metadata):
        return jsonify({"message": "Project created", "id": project_id, "project": metadata}), 201
    else:
        return jsonify({"error": "Project ID conflict"}), 409

@project_bp.route("/<project_id>", methods=["PUT"])
@require_login
def update_project(project_id):
    current_meta = repo.get_metadata(project_id)
    if not current_meta:
        return jsonify({"error": "Project not found"}), 404
    
    # Check permission
    user_id = session.get("user_id")
    role = session.get("role", 0)
    if current_meta.get("author_id") != user_id and role < ROLE_ADMIN:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    # Update fields
    fields = ["title", "description", "github_url", "demo_url", "image_url", "is_featured"]
    for field in fields:
        if field in data:
            current_meta[field] = data[field]
            
    repo.save_metadata(project_id, current_meta)
    return jsonify({"message": "Project updated", "project": current_meta})

@project_bp.route("/<project_id>", methods=["DELETE"])
@require_login
def delete_project(project_id):
    current_meta = repo.get_metadata(project_id)
    if not current_meta:
        return jsonify({"error": "Project not found"}), 404
        
    user_id = session.get("user_id")
    role = session.get("role", 0)
    if current_meta.get("author_id") != user_id and role < ROLE_ADMIN:
        return jsonify({"error": "Forbidden"}), 403

    repo.delete_item(project_id)
    return jsonify({"message": "Project deleted"})
