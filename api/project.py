from flask import Blueprint, jsonify, request
from decorators.decorators import token_role_required
from models.models import Project, db

project = Blueprint('project',__name__)

"""
    将项目对象转换为包含项目信息的字典
"""
def project_to_dict(project):
    return {
        'project_id': project.project_id,
        'title': project.title,
        'description': project.description,
        'thumbnail_url': project.thumbnail_url,
        'status': project.status,
        'creation_time': project.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        'creator_id': project.creator_id
    }

"""
    获取项目信息
"""
@project.route('/', methods=['GET'])
@project.route('/<int:project_id>', methods=['GET'])
def get_project(project_id = None):
    if project_id is not None:
        # 查询单个项目
        project = Project.query.filter_by(is_deleted=False).get(project_id)
        if project:
            # 返回单个项目的信息
            return jsonify(project_to_dict(project)), 200
        else:
            return jsonify({'message': 'Project not found'}), 404
    else:
        # 查询所有项目
        projects = Project.query.filter_by(is_deleted=False).all()
        # 返回所有项目的信息
        project_list = [project_to_dict(project) for project in projects]
        return jsonify({'projects': project_list}), 200

"""
    保存项目信息
"""
@project.route('/save', methods=['POST'])
@token_role_required("admin")
def save_project(current_user):
    # 获取 JSON 数据
    project_data = request.get_json()

    # 创建一个新项目
    save_project = Project(
        title = project_data.get('title'),
        description = project_data.get('description'),
        thumbnail_url = project_data.get('thumbnail_url'),
        creator_id = current_user.id
    )

    # 传了id就更新
    if project_data.get('id') is not None:
        update_project = Project.query.filter_by(is_deleted=False).get(project_data.get('id'))
        if update_project is None:
            return jsonify({'message': 'Project not found'}), 404
        update_project.title = save_project.title
        update_project.description = save_project.description
        update_project.thumbnail_url = save_project.thumbnail_url
    else:    
        # 将项目添加到数据库
        db.session.add(save_project)    
    db.session.commit()

    return jsonify({'message': 'Project saved successfully'}), 201


"""
    删除项目信息
"""
@project.route('/delete/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    # 获取要删除的项目
    project_to_delete = Project.query.filter_by(is_deleted=False).get(project_id)

    if project_to_delete:
        # 逻辑删除，将 is_deleted 设置为 True
        project_to_delete.is_deleted = True
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'}), 200
    else:
        return jsonify({'message': 'Project not found'}), 404