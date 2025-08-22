"""重构后的项目服务类
继承BaseService，大大减少重复代码
原来的项目相关代码分散在多个文件中，重构后集中管理
"""

from typing import Dict, List, Optional, Any
from .base_service import BaseService
from ..models import Project, User
from ..utils import save_file_to_user_data, delete_user_data_file
import os
import re
from urllib.parse import urlparse

class ProjectServiceRefactored(BaseService):
    """项目服务类 - 重构版本"""
    
    def __init__(self, db):
        super().__init__(db, Project)
        self.image_service = None  # 延迟初始化，避免循环导入
    
    def get_image_service(self):
        """获取图片服务实例"""
        if self.image_service is None:
            from .image_service import ImageService
            self.image_service = ImageService()
        return self.image_service
    
    # ========== 项目特定的查询方法 ==========
    
    def get_featured_projects(self, limit: int = 6) -> List[Project]:
        """获取精选项目"""
        return self.get_all(
            filters={'is_featured': True},
            order_by='-created_at',
            limit=limit
        )
    
    def get_user_projects(self, user_id: int, include_private: bool = False) -> List[Project]:
        """获取用户的项目"""
        filters = {'author_id': user_id}
        if not include_private:
            filters['is_public'] = True
        
        return self.get_all(
            filters=filters,
            order_by='-created_at'
        )
    
    def search_projects(self, search_term: str, filters: Optional[Dict] = None) -> List[Project]:
        """搜索项目"""
        search_fields = ['title', 'description']
        results = self.search(search_term, search_fields)
        
        # 应用额外过滤条件
        if filters:
            filtered_results = []
            for project in results:
                match = True
                for key, value in filters.items():
                    if hasattr(project, key) and getattr(project, key) != value:
                        match = False
                        break
                if match:
                    filtered_results.append(project)
            return filtered_results
        
        return results
    
    def get_projects_by_tag(self, tag: str) -> List[Project]:
        """根据标签获取项目（如果有标签系统）"""
        # 这里可以扩展标签功能
        return []
    
    # ========== 数据验证方法 ==========
    
    def validate_create_data(self, data: Dict) -> tuple[bool, str]:
        """验证创建项目数据"""
        # 必填字段检查
        required_fields = ['title', 'description', 'author_id']
        for field in required_fields:
            if not data.get(field):
                return False, f"缺少必填字段: {field}"
        
        # 标题长度检查
        title = data.get('title', '').strip()
        if len(title) < 1 or len(title) > 100:
            return False, "项目标题长度必须在1-100个字符之间"
        
        # 描述长度检查
        description = data.get('description', '').strip()
        if len(description) < 1 or len(description) > 1000:
            return False, "项目描述长度必须在1-1000个字符之间"
        
        # 检查标题是否重复
        existing = Project.query.filter_by(
            title=title, 
            author_id=data['author_id']
        ).first()
        if existing:
            return False, "您已经有同名的项目了"
        
        # URL格式验证
        url_fields = ['github_url', 'demo_url', 'image_url']
        for field in url_fields:
            url = data.get(field)
            if url and not self._is_valid_url_or_path(url):
                return False, f"无效的{field}格式"
        
        # GitHub URL特殊验证
        github_url = data.get('github_url')
        if github_url and not self._is_valid_github_url(github_url):
            return False, "无效的GitHub链接格式"
        
        return True, ""
    
    def validate_update_data(self, data: Dict, instance: Project) -> tuple[bool, str]:
        """验证更新项目数据"""
        # 基本验证（复用创建验证，但跳过重复检查）
        temp_data = data.copy()
        temp_data['author_id'] = instance.author_id  # 确保有author_id
        
        # 标题长度检查
        if 'title' in data:
            title = data['title'].strip()
            if len(title) < 1 or len(title) > 100:
                return False, "项目标题长度必须在1-100个字符之间"
            
            # 检查标题是否与其他项目重复（排除自己）
            existing = Project.query.filter(
                Project.title == title,
                Project.author_id == instance.author_id,
                Project.id != instance.id
            ).first()
            if existing:
                return False, "您已经有同名的项目了"
        
        # 描述长度检查
        if 'description' in data:
            description = data['description'].strip()
            if len(description) < 1 or len(description) > 1000:
                return False, "项目描述长度必须在1-1000个字符之间"
        
        # URL格式验证
        url_fields = ['github_url', 'demo_url', 'image_url']
        for field in url_fields:
            if field in data:
                url = data[field]
                if url and not self._is_valid_url_or_path(url):
                    return False, f"无效的{field}格式"
        
        # GitHub URL特殊验证
        if 'github_url' in data:
            github_url = data['github_url']
            if github_url and not self._is_valid_github_url(github_url):
                return False, "无效的GitHub链接格式"
        
        return True, ""
    
    # ========== 数据预处理方法 ==========
    
    def preprocess_create_data(self, data: Dict) -> Dict:
        """预处理创建数据"""
        processed = data.copy()
        
        # 清理字符串字段
        string_fields = ['title', 'description', 'github_url', 'demo_url', 'image_url']
        for field in string_fields:
            if field in processed and processed[field]:
                processed[field] = processed[field].strip()
        
        # 设置默认值
        processed.setdefault('is_featured', False)
        processed.setdefault('is_public', True)
        
        # 处理图片URL
        if processed.get('image_url'):
            processed['image_url'] = self._process_image_url(processed['image_url'])
        
        return processed
    
    def preprocess_update_data(self, data: Dict, instance: Project) -> Dict:
        """预处理更新数据"""
        processed = data.copy()
        
        # 清理字符串字段
        string_fields = ['title', 'description', 'github_url', 'demo_url', 'image_url']
        for field in string_fields:
            if field in processed and processed[field] is not None:
                processed[field] = processed[field].strip() if processed[field] else None
        
        # 处理图片URL
        if 'image_url' in processed and processed['image_url']:
            processed['image_url'] = self._process_image_url(processed['image_url'])
        
        return processed
    
    # ========== 后处理方法 ==========
    
    def postprocess_create(self, instance: Project, original_data: Dict):
        """创建后处理"""
        # 处理项目图片
        if instance.image_url:
            self._handle_project_image(instance)
        
        # 记录审计日志
        self._log_project_action('create', instance, original_data)
    
    def postprocess_update(self, instance: Project, original_data: Dict):
        """更新后处理"""
        # 处理项目图片变更
        if 'image_url' in original_data:
            self._handle_project_image(instance)
        
        # 记录审计日志
        self._log_project_action('update', instance, original_data)
    
    def can_delete(self, instance: Project) -> tuple[bool, str]:
        """检查是否可以删除项目"""
        # 检查是否有相关依赖（如评论、收藏等）
        # 这里可以根据实际业务需求添加检查逻辑
        return True, ""
    
    def preprocess_delete(self, instance: Project):
        """删除前处理"""
        # 清理项目相关文件
        if instance.image_url:
            self._cleanup_project_files(instance)
    
    def postprocess_delete(self, instance: Project):
        """删除后处理"""
        # 记录审计日志
        self._log_project_action('delete', instance, {})
    
    # ========== 项目特定的业务方法 ==========
    
    def toggle_featured(self, project_id: int) -> tuple[bool, str]:
        """切换项目精选状态"""
        project = self.get_by_id(project_id)
        if not project:
            return False, "项目不存在"
        
        project.is_featured = not project.is_featured
        
        try:
            self.db.session.commit()
            status = "精选" if project.is_featured else "普通"
            return True, f"项目已设置为{status}状态"
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"切换项目精选状态失败: {str(e)}")
            return False, "操作失败"
    
    def toggle_visibility(self, project_id: int) -> tuple[bool, str]:
        """切换项目可见性"""
        project = self.get_by_id(project_id)
        if not project:
            return False, "项目不存在"
        
        project.is_public = not project.is_public
        
        try:
            self.db.session.commit()
            status = "公开" if project.is_public else "私有"
            return True, f"项目已设置为{status}状态"
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"切换项目可见性失败: {str(e)}")
            return False, "操作失败"
    
    # ========== 私有工具方法 ==========
    
    def _is_valid_url_or_path(self, url: str) -> bool:
        """验证URL或文件路径格式"""
        if not url:
            return True
        
        # 检查是否为有效URL
        try:
            result = urlparse(url)
            if result.scheme in ['http', 'https']:
                return True
        except:
            pass
        
        # 检查是否为文件路径
        if url.startswith('file://') or '/' in url or '\\' in url or '.' in url:
            return True
        
        return False
    
    def _is_valid_github_url(self, url: str) -> bool:
        """验证GitHub URL格式"""
        if not url:
            return True
        
        github_pattern = r'^https://github\.com/[\w\-\.]+/[\w\-\.]+/?$'
        return bool(re.match(github_pattern, url))
    
    def _process_image_url(self, image_url: str) -> str:
        """处理图片URL"""
        if not image_url:
            return image_url
        
        # 这里可以添加图片URL的处理逻辑
        # 比如转换相对路径、验证图片存在性等
        return image_url
    
    def _handle_project_image(self, project: Project):
        """处理项目图片"""
        # 这里可以添加图片处理逻辑
        # 比如生成缩略图、压缩图片等
        pass
    
    def _cleanup_project_files(self, project: Project):
        """清理项目相关文件"""
        # 清理项目图片文件
        if project.image_url:
            # 这里添加文件清理逻辑
            pass
    
    def _log_project_action(self, action: str, project: Project, data: Dict):
        """记录项目操作日志"""
        self.logger.info(
            f"项目{action}: ID={project.id}, 标题={project.title}, "
            f"作者={project.author_id}, 数据={data}"
        )

# 使用示例：
# project_service = ProjectServiceRefactored(db)
# success, result = project_service.create({
#     'title': '新项目',
#     'description': '项目描述',
#     'author_id': 1
# })