// 添加项目
document.getElementById('addProjectForm').addEventListener('submit', function (e) {
    e.preventDefault()

    const formData = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        github_url: document.getElementById('projectGithub').value,
        demo_url: document.getElementById('projectDemo').value,
        image_url: document.getElementById('projectImage').value,
        is_featured: document.getElementById('projectFeatured').checked
    }

    fetch('/api/projects', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert('项目创建成功！')
                location.reload()
            } else {
                alert('创建失败：' + data.message)
            }
        })
        .catch((error) => {
            console.error('Error:', error)
            alert('创建失败，请重试')
        })
})

// 编辑项目表单提交
document.getElementById('editProjectForm').addEventListener('submit', function (e) {
    e.preventDefault()

    const projectId = document.getElementById('editProjectId').value
    const formData = {
        title: document.getElementById('editProjectTitle').value,
        description: document.getElementById('editProjectDescription').value,
        github_url: document.getElementById('editProjectGithub').value,
        demo_url: document.getElementById('editProjectDemo').value,
        image_url: document.getElementById('editProjectImage').value,
        is_featured: document.getElementById('editProjectFeatured').checked
    }

    fetch(`/api/projects/${projectId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert('项目更新成功！')
                location.reload()
            } else {
                alert('更新失败：' + data.message)
            }
        })
        .catch((error) => {
            console.error('Error:', error)
            alert('更新失败，请重试')
        })
})

// 切换精选状态
function toggleFeatured(projectId, currentStatus) {
    if (confirm('确定要切换项目的精选状态吗？')) {
        fetch(`/api/projects/${projectId}/featured`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_featured: !currentStatus })
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    location.reload()
                } else {
                    alert('操作失败：' + data.message)
                }
            })
            .catch((error) => {
                console.error('Error:', error)
                alert('操作失败，请重试')
            })
    }
}

// 编辑项目
function editProject(projectId) {
    // 获取项目详情
    fetch(`/api/projects/${projectId}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const project = data.project

                // 填充表单
                document.getElementById('editProjectId').value = project.id
                document.getElementById('editProjectTitle').value = project.title
                document.getElementById('editProjectDescription').value = project.description
                document.getElementById('editProjectGithub').value = project.github_url || ''
                document.getElementById('editProjectDemo').value = project.demo_url || ''
                document.getElementById('editProjectImage').value = project.image_url || ''
                document.getElementById('editProjectFeatured').checked = project.is_featured

                // 显示模态框
                new bootstrap.Modal(document.getElementById('editProjectModal')).show()
            } else {
                alert('获取项目详情失败：' + data.message)
            }
        })
        .catch((error) => {
            console.error('Error:', error)
            alert('获取项目详情失败，请重试')
        })
}

// 删除项目
function deleteProject(projectId) {
    if (confirm('确定要删除这个项目吗？此操作不可恢复！')) {
        fetch(`/api/projects/${projectId}`, {
            method: 'DELETE'
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert('项目删除成功！')
                    location.reload()
                } else {
                    alert('删除失败：' + data.message)
                }
            })
            .catch((error) => {
                console.error('Error:', error)
                alert('删除失败，请重试')
            })
    }
}