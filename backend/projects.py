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
    send_from_directory,
)
from werkzeug.utils import secure_filename
from .models import db, Project, User
from .config import ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_GUEST
from .utils import (
    require_role,
    can_manage_project,
    validate_csrf_token,
    save_file_to_user_data,
    delete_user_data_file,
    create_project_folder,
    save_project_metadata,
    load_project_metadata,
    delete_project_folder,
    get_project_folder_path,
    get_project_files,
)

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/api/projects", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_project():
    data = request.get_json()

    # 处理图片URL - 不再使用缓存，直接保存到项目文件夹
    image_url = data.get("image_url")
    # 暂时保存原始URL，稍后在项目文件夹创建后处理

    project = Project(
        title=data["title"],
        description=data["description"],
        github_url=data.get("github_url"),
        demo_url=data.get("demo_url"),
        image_url=image_url,
        is_featured=data.get("is_featured", False),
        author_id=session["user_id"],
    )
    db.session.add(project)
    db.session.commit()

    try:
        # 创建项目文件夹
        project_path, folder_name = create_project_folder(
            project.id, project.created_at
        )
        if project_path:
            # 保存项目元数据
            project_metadata = {
                "title": project.title,
                "description": project.description,
                "github_url": project.github_url,
                "demo_url": project.demo_url,
            }
            save_project_metadata(project_path, project_metadata)

            # 创建默认的readme.md文件
            readme_content = f"# {project.title}\n\n{project.description}\n\n## 项目简介\n\n这是 {project.title} 项目的文档空间。\n\n## GitHub 仓库\n\n{project.github_url if project.github_url else '暂未设置'}\n\n## 演示地址\n\n{project.demo_url if project.demo_url else '暂未设置'}"
            readme_path = os.path.join(project_path, "readme.md")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)

            # 如果有图片URL，直接下载到项目文件夹
            if image_url:
                try:
                    import requests
                    from urllib.parse import urlparse
                    import uuid

                    # 处理本地文件URI
                    if image_url.startswith("file://"):
                        from urllib.parse import unquote

                        local_path = unquote(urlparse(image_url).path)
                        if os.name == "nt" and local_path.startswith("/"):
                            local_path = local_path[1:]

                        if os.path.exists(local_path):
                            ext = os.path.splitext(local_path)[1] or ".jpg"
                            project_image_path = os.path.join(
                                project_path, f"index{ext}"
                            )
                            shutil.copy2(local_path, project_image_path)
                            # 更新数据库中的image_url为相对路径
                            project.image_url = f"index{ext}"

                    # 处理网络URL
                    elif image_url.startswith(("http://", "https://")):
                        response = requests.get(image_url, stream=True, timeout=10)
                        response.raise_for_status()

                        # 获取文件扩展名
                        content_type = response.headers.get("Content-Type")
                        if content_type and "image" in content_type:
                            ext = "." + content_type.split("/")[1].split(";")[0]
                        else:
                            ext = (
                                os.path.splitext(urlparse(image_url).path)[1] or ".jpg"
                            )

                        project_image_path = os.path.join(project_path, f"index{ext}")
                        with open(project_image_path, "wb") as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)

                        # 更新数据库中的image_url为相对路径
                        project.image_url = f"index{ext}"

                    # 处理已经是用户数据URL的情况（向后兼容）
                    elif image_url.startswith("/user_data/"):
                        user_data_file = image_url.replace("/user_data/", "")
                        user_data_path = os.path.join(
                            current_app.root_path, "user_data", user_data_file
                        )
                        if os.path.exists(user_data_path):
                            ext = os.path.splitext(user_data_file)[1] or ".jpg"
                            project_image_path = os.path.join(
                                project_path, f"index{ext}"
                            )
                            shutil.copy2(user_data_path, project_image_path)
                            # 更新数据库中的image_url为相对路径
                            project.image_url = f"index{ext}"

                except Exception as e:
                    current_app.logger.error(f"Failed to download project image: {e}")
                    # 如果下载失败，清空image_url
                    project.image_url = None

        # 项目文件夹创建完成
        db.session.commit()

    except Exception as e:
        current_app.logger.error(f"Failed to create project folder: {e}")
        # 即使文件夹创建失败，项目仍然创建成功

    return jsonify(
        {"success": True, "message": "项目创建成功", "project_id": project.id}
    )


@projects_bp.route("/api/projects/<int:project_id>", methods=["PUT", "DELETE"])
@require_role(ROLE_MEMBER)
def manage_project(project_id):
    project = Project.query.get_or_404(project_id)
    current_user = User.query.get(session["user_id"])
    if project.author_id != session["user_id"] and current_user.role < ROLE_ADMIN:
        return jsonify({"success": False, "message": "权限不足"}), 403

    if request.method == "PUT":
        data = request.get_json()

        # 处理图片URL - 实现白名单机制
        new_image_url = data.get("image_url")

        # 获取项目文件夹路径
        project_path = get_project_folder_path(project.id, project.created_at)

        # 检查是否需要更新图片
        if new_image_url != project.image_url:
            # 白名单检查：如果新URL是index.*格式，则保持不变
            if new_image_url and new_image_url.startswith("index."):
                # index.*格式的URL放行，不做更改
                project.image_url = new_image_url
            elif not new_image_url:  # 如果新URL为空
                # 清空项目头图
                project.image_url = None

                # 删除项目文件夹中的index.*文件
                if project_path and os.path.exists(project_path):
                    try:
                        import glob

                        index_files = glob.glob(os.path.join(project_path, "index.*"))
                        for index_file in index_files:
                            if os.path.isfile(index_file):
                                os.remove(index_file)
                                current_app.logger.info(
                                    f"Deleted project image: {index_file}"
                                )
                    except Exception as e:
                        current_app.logger.error(f"Failed to delete index files: {e}")
            else:
                # 处理其他URL（网络URL、本地文件等）
                try:
                    import requests
                    from urllib.parse import urlparse

                    # 处理本地文件URI
                    if new_image_url.startswith("file://"):
                        from urllib.parse import unquote

                        local_path = unquote(urlparse(new_image_url).path)
                        if os.name == "nt" and local_path.startswith("/"):
                            local_path = local_path[1:]

                        if os.path.exists(local_path) and project_path:
                            # 删除旧的index.*文件
                            import glob

                            old_index_files = glob.glob(
                                os.path.join(project_path, "index.*")
                            )
                            for old_file in old_index_files:
                                if os.path.isfile(old_file):
                                    os.remove(old_file)

                            ext = os.path.splitext(local_path)[1] or ".jpg"
                            project_image_path = os.path.join(
                                project_path, f"index{ext}"
                            )
                            shutil.copy2(local_path, project_image_path)
                            project.image_url = f"index{ext}"

                    # 处理网络URL
                    elif new_image_url.startswith(("http://", "https://")):
                        if project_path:
                            response = requests.get(
                                new_image_url, stream=True, timeout=10
                            )
                            response.raise_for_status()

                            # 删除旧的index.*文件
                            import glob

                            old_index_files = glob.glob(
                                os.path.join(project_path, "index.*")
                            )
                            for old_file in old_index_files:
                                if os.path.isfile(old_file):
                                    os.remove(old_file)

                            # 获取文件扩展名
                            content_type = response.headers.get("Content-Type")
                            if content_type and "image" in content_type:
                                ext = "." + content_type.split("/")[1].split(";")[0]
                            else:
                                ext = (
                                    os.path.splitext(urlparse(new_image_url).path)[1]
                                    or ".jpg"
                                )

                            project_image_path = os.path.join(
                                project_path, f"index{ext}"
                            )
                            with open(project_image_path, "wb") as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)

                            project.image_url = f"index{ext}"

                    # 处理已经是用户数据URL的情况（向后兼容）
                    elif new_image_url.startswith("/user_data/"):
                        user_data_file = new_image_url.replace("/user_data/", "")
                        user_data_path = os.path.join(
                            current_app.root_path, "user_data", user_data_file
                        )
                        if os.path.exists(user_data_path) and project_path:
                            # 删除旧的index.*文件
                            import glob

                            old_index_files = glob.glob(
                                os.path.join(project_path, "index.*")
                            )
                            for old_file in old_index_files:
                                if os.path.isfile(old_file):
                                    os.remove(old_file)

                            ext = os.path.splitext(user_data_file)[1] or ".jpg"
                            project_image_path = os.path.join(
                                project_path, f"index{ext}"
                            )
                            shutil.copy2(user_data_path, project_image_path)
                            project.image_url = f"index{ext}"

                except Exception as e:
                    current_app.logger.error(f"Failed to process project image: {e}")
                    # 如果处理失败，保持原有的image_url不变
                    pass

        # 更新数据库中的项目信息
        old_title = project.title
        project.title = data.get("title", project.title)
        project.description = data.get("description", project.description)
        project.github_url = data.get("github_url", project.github_url)
        project.demo_url = data.get("demo_url", project.demo_url)
        project.is_featured = data.get("is_featured", project.is_featured)
        db.session.commit()

        # 更新项目文件夹中的元数据
        try:
            project_path = get_project_folder_path(project.id, project.created_at)
            if os.path.exists(project_path):
                # 更新项目元数据
                project_metadata = {
                    "title": project.title,
                    "description": project.description,
                    "github_url": project.github_url,
                    "demo_url": project.demo_url,
                }
                save_project_metadata(project_path, project_metadata)

                # 如果标题发生变化，更新readme.md文件
                if old_title != project.title:
                    readme_path = os.path.join(project_path, "readme.md")
                    if os.path.exists(readme_path):
                        with open(readme_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        # 替换标题
                        content = content.replace(
                            f"# {old_title}", f"# {project.title}", 1
                        )
                        content = content.replace(
                            f"这是 {old_title} 项目的文档空间",
                            f"这是 {project.title} 项目的文档空间",
                        )
                        with open(readme_path, "w", encoding="utf-8") as f:
                            f.write(content)
        except Exception as e:
            current_app.logger.error(f"Failed to update project metadata: {e}")

        return jsonify({"success": True, "message": "项目更新成功"})

    if request.method == "DELETE":
        # 删除项目文件夹
        try:
            delete_project_folder(project.id, project.created_at)
        except Exception as e:
            current_app.logger.error(f"Failed to delete project folder: {e}")

        db.session.delete(project)
        db.session.commit()
        return jsonify({"success": True, "message": "项目删除成功"})


@projects_bp.route("/projects/<int:project_id>/docs")
def project_docs(project_id):
    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 检查用户是否登录
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        flash("该项目文档空间不存在", "error")
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
    # 获取项目文件夹中的所有文件
    all_files = get_project_files(project_docs_path)

    # 分离.md文件和其他文件
    md_files = [f for f in all_files if f.get("is_markdown", False)]
    other_files = [f for f in all_files if not f.get("is_markdown", False)]

    # 为了与模板兼容，将modified_time重命名为modified，并添加relative_path字段
    for file in md_files:
        file["modified"] = file.get("modified_time", datetime.min)
        file["relative_path"] = file["name"]  # 对于文档文件，相对路径就是文件名
    for file in other_files:
        file["modified"] = file.get("modified_time", datetime.min)
        file["relative_path"] = file["name"]  # 对于其他文件，相对路径就是文件名

    # 按修改时间排序，最新的在前
    md_files.sort(key=lambda x: x.get("modified", datetime.min), reverse=True)
    other_files.sort(
        key=lambda x: (
            x.get("modified", datetime.min) if x["type"] == "file" else datetime.min
        ),
        reverse=True,
    )

    return render_template(
        "project_docs_list.html",
        project=project,
        md_files=md_files,
        other_files=other_files,
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

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        flash("该项目文档空间不存在", "error")
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

        # 创建自定义渲染器来处理图片路径
        class ProjectImageRenderer(mistune.HTMLRenderer):
            def __init__(self, project_id):
                super().__init__()
                self.project_id = project_id
            
            def image(self, alt, url, title=None):
                # 如果是相对路径（不以http://、https://、/开头），则补全为项目图片路径
                if not url.startswith(('http://', 'https://', '/')):
                    url = url_for('projects.project_image', project_id=self.project_id, filename=url)
                
                # 构建img标签
                img_attrs = f'src="{url}"'
                if alt:
                    img_attrs += f' alt="{alt}"'
                if title:
                    img_attrs += f' title="{title}"'
                
                return f'<img {img_attrs} />'
        
        # 使用自定义渲染器解析Markdown
        renderer = ProjectImageRenderer(project_id)
        markdown = mistune.Markdown(renderer=renderer)
        html_content = markdown(content)

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

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目文档空间不存在"}), 400

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

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目文档空间不存在"}), 400

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

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)
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

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目文档空间不存在"}), 400

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

    # 获取项目文件夹路径
    project_docs_path = get_project_folder_path(project.id, project.created_at)

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目文档空间不存在"}), 400

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

    # 处理图片URL - 实现白名单机制
    new_image_url = data.get("image_url")

    # 获取项目文件夹路径
    project_path = get_project_folder_path(project.id, project.created_at)

    # 检查是否需要更新图片
    if new_image_url != project.image_url:
        # 白名单检查：如果新URL是index.*格式，则保持不变
        if new_image_url and new_image_url.startswith("index."):
            # index.*格式的URL放行，不做更改
            project.image_url = new_image_url
        elif not new_image_url:  # 如果新URL为空
            # 清空项目头图
            project.image_url = None

            # 删除项目文件夹中的index.*文件
            if project_path and os.path.exists(project_path):
                try:
                    import glob

                    index_files = glob.glob(os.path.join(project_path, "index.*"))
                    for index_file in index_files:
                        if os.path.isfile(index_file):
                            os.remove(index_file)
                            current_app.logger.info(
                                f"Deleted project image: {index_file}"
                            )
                except Exception as e:
                    current_app.logger.error(f"Failed to delete index files: {e}")
        else:
            # 处理其他URL（网络URL、本地文件等）
            try:
                import requests
                from urllib.parse import urlparse

                # 处理本地文件URI
                if new_image_url.startswith("file://"):
                    from urllib.parse import unquote

                    local_path = unquote(urlparse(new_image_url).path)
                    if os.name == "nt" and local_path.startswith("/"):
                        local_path = local_path[1:]

                    if os.path.exists(local_path) and project_path:
                        # 删除旧的index.*文件
                        import glob

                        old_index_files = glob.glob(
                            os.path.join(project_path, "index.*")
                        )
                        for old_file in old_index_files:
                            if os.path.isfile(old_file):
                                os.remove(old_file)

                        ext = os.path.splitext(local_path)[1] or ".jpg"
                        project_image_path = os.path.join(project_path, f"index{ext}")
                        shutil.copy2(local_path, project_image_path)
                        project.image_url = f"index{ext}"

                # 处理网络URL
                elif new_image_url.startswith(("http://", "https://")):
                    if project_path:
                        response = requests.get(new_image_url, stream=True, timeout=10)
                        response.raise_for_status()

                        # 删除旧的index.*文件
                        import glob

                        old_index_files = glob.glob(
                            os.path.join(project_path, "index.*")
                        )
                        for old_file in old_index_files:
                            if os.path.isfile(old_file):
                                os.remove(old_file)

                        # 获取文件扩展名
                        content_type = response.headers.get("Content-Type")
                        if content_type and "image" in content_type:
                            ext = "." + content_type.split("/")[1].split(";")[0]
                        else:
                            ext = (
                                os.path.splitext(urlparse(new_image_url).path)[1]
                                or ".jpg"
                            )

                        project_image_path = os.path.join(project_path, f"index{ext}")
                        with open(project_image_path, "wb") as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)

                        project.image_url = f"index{ext}"

                # 处理已经是用户数据URL的情况（向后兼容）
                elif new_image_url.startswith("/user_data/"):
                    user_data_file = new_image_url.replace("/user_data/", "")
                    user_data_path = os.path.join(
                        current_app.root_path, "user_data", user_data_file
                    )
                    if os.path.exists(user_data_path) and project_path:
                        # 删除旧的index.*文件
                        import glob

                        old_index_files = glob.glob(
                            os.path.join(project_path, "index.*")
                        )
                        for old_file in old_index_files:
                            if os.path.isfile(old_file):
                                os.remove(old_file)

                        ext = os.path.splitext(user_data_file)[1] or ".jpg"
                        project_image_path = os.path.join(project_path, f"index{ext}")
                        shutil.copy2(user_data_path, project_image_path)
                        project.image_url = f"index{ext}"

            except Exception as e:
                current_app.logger.error(f"Failed to process project image: {e}")
                # 如果处理失败，保持原有的image_url不变
                pass

    # 更新项目信息
    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.github_url = data.get("github_url", project.github_url)
    project.demo_url = data.get("demo_url", project.demo_url)
    project.is_featured = data.get("is_featured", project.is_featured)

    db.session.commit()

    return jsonify({"success": True, "message": "项目更新成功"})


@projects_bp.route("/projects/<int:project_id>/download/<path:filename>")
def download_project_file(project_id, filename):
    """下载项目文件"""
    project = Project.query.get_or_404(project_id)

    # 获取项目文件夹路径
    project_path = get_project_folder_path(project.id, project.created_at)

    if not os.path.exists(project_path):
        return jsonify({"error": "项目文件夹不存在"}), 404

    # 安全检查：确保文件在项目文件夹内
    file_path = os.path.join(project_path, filename)
    if not os.path.commonpath([project_path, file_path]) == project_path:
        return jsonify({"error": "非法文件路径"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "文件不存在"}), 404

    if os.path.isdir(file_path):
        return jsonify({"error": "无法下载文件夹"}), 400

    return send_from_directory(project_path, filename, as_attachment=True)


@projects_bp.route("/projects/<int:project_id>/image/<path:filename>")
def project_image(project_id, filename):
    """提供项目图片"""
    project = Project.query.get_or_404(project_id)

    # 获取项目文件夹路径
    project_path = get_project_folder_path(project.id, project.created_at)

    if not os.path.exists(project_path):
        return jsonify({"error": "项目文件夹不存在"}), 404

    # 安全检查：确保文件在项目文件夹内
    file_path = os.path.join(project_path, filename)
    if not os.path.commonpath([project_path, file_path]) == project_path:
        return jsonify({"error": "非法文件路径"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "文件不存在"}), 404

    if os.path.isdir(file_path):
        return jsonify({"error": "无法访问文件夹"}), 400

    return send_from_directory(project_path, filename)
