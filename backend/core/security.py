import functools
from flask import session, jsonify, current_app
from backend.config import ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN

def require_role(role):
    """
    Decorator to check if the current user has the required role.
    Returns 401 if not logged in, 403 if insufficient permissions.
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"error": "Unauthorized", "message": "Please login first"}), 401
            
            user_role = session.get("role", ROLE_GUEST)
            
            if user_role < role:
                return jsonify({"error": "Forbidden", "message": "Insufficient permissions"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_login(f):
    return require_role(ROLE_MEMBER)(f)

def require_admin(f):
    return require_role(ROLE_ADMIN)(f)

def require_super_admin(f):
    return require_role(ROLE_SUPER_ADMIN)(f)
