# 认证相关路由

from flask import Blueprint, jsonify, request, session

from backend.config import ROLE_GUEST
from backend.core.Security import require_login
from backend.data.models.user import User
from backend.data import users

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    pass


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """注销当前登录用户"""
    pass


@auth_bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    pass


@auth_bp.route("/me", methods=["GET"])
@require_login
def get_current_user():
    """获取当前登录用户的信息"""
    pass
