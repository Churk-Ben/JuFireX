import os
import shutil
import mistune
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    current_app,
)
from werkzeug.utils import secure_filename
from .models import db, Project, User
from .config import ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_GUEST
from .utils import require_role, can_manage_project, validate_csrf_token

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/api/projects", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_project():
    data = request.get_json()
    project = Project(
        title=data["title"],
        description=data["description"],
        github_url=data.get("github_url"),
        demo_url=data.get("demo_url"),
        image_url=data.get("image_url"),
        is_featured=data.get("is_featured", False),
        author_id=session["user_id"],
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(
        {"success": True, "message": "项目创建成功", "project_id": project.id}
    )


@projects_bp.route("/api/projects/<int:project_id>/open-docs", methods=["POST"])
@require_role(ROLE_MEMBER)
def open_project_docs(project_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return (
            jsonify({"success": False, "message": "只有项目创建者可以开通文档空间"}),
            403,
        )

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    projects_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projects"
    )
    project_docs_path = os.path.join(projects_dir, folder_name)

    # 检查文件夹是否已存在
    if os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目的文档空间已存在"}), 400

    try:
        # 确保projects目录存在
        os.makedirs(projects_dir, exist_ok=True)
        # 创建项目文档目录
        os.makedirs(project_docs_path)

        # 创建默认的readme.md文件
        readme_content = f"# {project.title} 文档\n\n欢迎使用 {project.title} 项目文档！\n\n## 项目简介\n\n{project.description}\n\n## 文档说明\n\n这是项目的文档空间，您可以在这里添加和管理项目相关的文档。"
        readme_path = os.path.join(project_docs_path, "readme.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 更新项目的docs_opened字段
        project.docs_opened = True
        db.session.commit()

        return jsonify({"success": True, "message": "文档空间开通成功"})
    except Exception as e:
        return (
            jsonify({"success": False, "message": f"创建文档空间失败: {str(e)}"}),
            500,
        )


@projects_bp.route("/projects/<int:project_id>/docs")
def project_docs(project_id):
    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 检查用户是否登录
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        flash("该项目尚未开通文档空间", "error")
        return redirect(url_for("index"))

    # 如果用户未登录，尝试直接访问readme.md
    if not current_user:
        # 查找readme文件（不区分大小写）
        readme_files = []
        for file in os.listdir(project_docs_path):
            if file.lower() in ["readme.md", "readme.markdown"]:
                readme_files.append(file)

        if readme_files:
            # 如果找到readme文件，直接重定向到文档查看页面
            return redirect(
                url_for(
                    "projects.project_doc_view",
                    project_id=project_id,
                    filename=readme_files[0],
                )
            )
        else:
            # 如果没有readme文件，提示用户登录查看文档列表
            flash("该项目没有公开的readme文档，请登录查看完整文档列表", "info")
            return redirect(url_for("auth.login"))

    # 用户已登录，显示完整的文档列表
    # 获取所有.md文件
    md_files = []
    for file in os.listdir(project_docs_path):
        if file.endswith(".md"):
            file_path = os.path.join(project_docs_path, file)
            # 获取文件修改时间
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            md_files.append({"name": file, "path": file, "modified": mod_time})

    # 按修改时间排序，最新的在前
    md_files.sort(key=lambda x: x["modified"], reverse=True)

    return render_template(
        "project_docs_list.html",
        project=project,
        md_files=md_files,
        current_user=current_user,
    )


@projects_bp.route("/projects/<int:project_id>/docs/<path:filename>")
def project_doc_view(project_id, filename):
    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 检查用户是否登录
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        flash("该项目尚未开通文档空间", "error")
        return redirect(url_for("index"))

    # 构建文件完整路径
    file_path = os.path.join(project_docs_path, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        flash(f"文件 {filename} 不存在", "error")
        return redirect(url_for("projects.project_docs", project_id=project_id))

    try:
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 使用mistune解析Markdown
        html_content = mistune.html(content)

        return render_template(
            "project_doc_view.html",
            project=project,
            filename=filename,
            content=content,
            html_content=html_content,
            current_user=current_user,
        )
    except Exception as e:
        flash(f"读取文件失败: {str(e)}", "error")
        return redirect(url_for("projects.project_docs", project_id=project_id))


@projects_bp.route("/api/projects/<int:project_id>/docs/upload", methods=["POST"])
@require_role(ROLE_MEMBER)
def upload_project_doc(project_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以上传文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    try:
        # 获取上传的文件和文档名称
        doc_file = request.files.get("docFile")
        doc_name = request.form.get("docName")

        if not doc_file or not doc_name:
            return jsonify({"success": False, "message": "缺少必要参数"}), 400

        # 验证文件类型
        if not doc_file.filename.lower().endswith((".md", ".markdown")):
            return (
                jsonify({"success": False, "message": "只支持Markdown格式的文档"}),
                400,
            )

        # 清理文件名，确保安全
        safe_doc_name = secure_filename(doc_name)
        if not safe_doc_name:
            return jsonify({"success": False, "message": "无效的文档名称"}), 400

        # 添加.md扩展名
        if not safe_doc_name.lower().endswith(".md"):
            safe_doc_name += ".md"

        # 检查文件是否已存在
        file_path = os.path.join(project_docs_path, safe_doc_name)
        if os.path.exists(file_path):
            return jsonify({"success": False, "message": "同名文档已存在"}), 400

        # 读取文件内容并保存
        content = doc_file.read().decode("utf-8")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return jsonify(
            {"success": True, "message": "文档上传成功", "filename": safe_doc_name}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"上传文档失败: {str(e)}"}), 500


@projects_bp.route("/api/projects/<int:project_id>/docs/create", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_project_doc(project_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以创建文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    try:
        # 获取文档标题和内容
        data = request.json
        doc_title = data.get("docTitle")
        doc_content = data.get("docContent")

        if not doc_title or not doc_content:
            return jsonify({"success": False, "message": "缺少必要参数"}), 400

        # 清理文件名，确保安全
        safe_doc_name = secure_filename(doc_title)
        if not safe_doc_name:
            return jsonify({"success": False, "message": "无效的文档标题"}), 400

        # 添加.md扩展名
        if not safe_doc_name.lower().endswith(".md"):
            safe_doc_name += ".md"

        # 检查文件是否已存在
        file_path = os.path.join(project_docs_path, safe_doc_name)
        if os.path.exists(file_path):
            return jsonify({"success": False, "message": "同名文档已存在"}), 400

        # 保存文档内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        return jsonify(
            {"success": True, "message": "文档创建成功", "filename": safe_doc_name}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"创建文档失败: {str(e)}"}), 500


@projects_bp.route(
    "/api/projects/<int:project_id>/docs/<path:filename>/raw", methods=["GET"]
)
@require_role(ROLE_MEMBER)
def get_project_doc_raw(project_id, filename):
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"success": False, "message": "项目不存在"}), 404

    # 权限检查：只有项目作者或管理员可以获取
    user = db.session.get(User, session.get("user_id"))
    if not user or (user.id != project.author_id and user.role < ROLE_ADMIN):
        return jsonify({"success": False, "message": "权限不足"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )
    doc_path = os.path.join(project_docs_path, filename)

    if not os.path.exists(doc_path) or not os.path.isfile(doc_path):
        return jsonify({"success": False, "message": "文档不存在"}), 404

    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"success": True, "content": content})
    except Exception as e:
        return jsonify({"success": False, "message": f"读取文件时出错: {e}"}), 500


@projects_bp.route(
    "/api/projects/<int:project_id>/docs/<path:filename>", methods=["PUT"]
)
@require_role(ROLE_MEMBER)
def update_project_doc(project_id, filename):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以编辑文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    # 构建文件完整路径
    file_path = os.path.join(project_docs_path, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"success": False, "message": f"文件 {filename} 不存在"}), 404

    try:
        # 获取更新的文档标题和内容
        data = request.json
        new_doc_title = data.get("docTitle")
        doc_content = data.get("docContent")

        if not new_doc_title or not doc_content:
            return jsonify({"success": False, "message": "缺少必要参数"}), 400

        # 清理文件名，确保安全
        safe_doc_name = secure_filename(new_doc_title)
        if not safe_doc_name:
            return jsonify({"success": False, "message": "无效的文档标题"}), 400

        # 添加.md扩展名
        if not safe_doc_name.lower().endswith(".md"):
            safe_doc_name += ".md"

        # 检查是否需要重命名文件
        new_file_path = os.path.join(project_docs_path, safe_doc_name)
        rename_needed = filename != safe_doc_name

        # 如果需要重命名，检查新文件名是否已存在
        if rename_needed and os.path.exists(new_file_path):
            return jsonify({"success": False, "message": "同名文档已存在"}), 400

        # 保存文档内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        # 如果需要重命名，执行重命名操作
        if rename_needed:
            os.rename(file_path, new_file_path)
            return jsonify(
                {
                    "success": True,
                    "message": "文档更新并重命名成功",
                    "filename": safe_doc_name,
                }
            )

        return jsonify(
            {"success": True, "message": "文档更新成功", "filename": filename}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"更新文档失败: {str(e)}"}), 500


@projects_bp.route(
    "/api/projects/<int:project_id>/docs/<path:filename>", methods=["DELETE"]
)
@require_role(ROLE_MEMBER)
def delete_project_doc(project_id, filename):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以删除文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "projects",
        folder_name,
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    # 构建文件完整路径
    file_path = os.path.join(project_docs_path, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"success": False, "message": f"文件 {filename} 不存在"}), 404

    try:
        # 删除文件
        os.remove(file_path)
        return jsonify({"success": True, "message": "文档删除成功"})
    except Exception as e:
        return jsonify({"success": False, "message": f"删除文档失败: {str(e)}"}), 500


@projects_bp.route("/api/projects/<int:project_id>/featured", methods=["PUT"])
@require_role(ROLE_ADMIN)
def toggle_project_featured(project_id):
    data = request.get_json()
    project = Project.query.get_or_404(project_id)
    project.is_featured = data["is_featured"]
    db.session.commit()
    return jsonify({"success": True, "message": "项目状态更新成功"})


@projects_bp.route("/api/projects/<int:project_id>", methods=["GET"])
@require_role(ROLE_ADMIN)
def get_project(project_id):
    project = Project.query.get_or_404(project_id)

    # 构建项目数据
    project_data = {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "github_url": project.github_url,
        "demo_url": project.demo_url,
        "image_url": project.image_url,
        "is_featured": project.is_featured,
        "created_at": project.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "author_id": project.author_id,
        "author": project.author.username if project.author else None,
    }

    return jsonify({"success": True, "project": project_data})


@projects_bp.route("/api/projects/<int:project_id>", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    # 检查权限：只有项目作者或超级管理员可以更新
    if (
        project.author_id != session["user_id"]
        and session.get("role", 0) < ROLE_SUPER_ADMIN
    ):
        return jsonify({"success": False, "message": "权限不足"})

    data = request.get_json()

    # 更新项目信息
    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.github_url = data.get("github_url", project.github_url)
    project.demo_url = data.get("demo_url", project.demo_url)
    project.image_url = data.get("image_url", project.image_url)
    project.is_featured = data.get("is_featured", project.is_featured)

    db.session.commit()

    return jsonify({"success": True, "message": "项目更新成功"})


@projects_bp.route("/api/projects/<int:project_id>", methods=["DELETE"])
@require_role(ROLE_MEMBER, owner_check=can_manage_project)
def delete_project(project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"success": False, "message": "项目不存在"}), 404

    try:
        # 删除项目文档空间
        if project.docs_opened:
            date_str = project.created_at.strftime("%Y%m%d")
            project_folder_name = f"{date_str}-{project.id}"
            project_path = os.path.join(
                current_app.config["PROJECTS_FOLDER"], project_folder_name
            )
            if os.path.exists(project_path):
                shutil.rmtree(project_path)

        db.session.delete(project)
        db.session.commit()
        return jsonify({"success": True, "message": "项目已删除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500
