from flask import Blueprint, jsonify, request
from decorators.decorators import token_role_required
from models.models import Feedback, db

feedback = Blueprint('feedback',__name__)

"""
    获取反馈信息
"""
@feedback.route('/', methods=['GET'])
@feedback.route('/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id = None):
    if feedback_id is not None:
        # 查询单个反馈
        feedback = Feedback.query.filter_by(is_deleted=False).get(feedback_id)
        if feedback:
            # 返回单个反馈的信息
            return jsonify(feedback.serialize()), 200
        else:
            return jsonify({'message': 'Feedback not found'}), 404
    else:
        # 查询所有反馈
        feedbacks = Feedback.query.filter_by(is_deleted=False).all()
        # 返回所有反馈的信息
        feedback_list = [feedback.serialize() for feedback in feedbacks]
        return jsonify({'feedbacks': feedback_list}), 200

"""
    保存反馈信息
"""
@feedback.route('/save', methods=['POST'])
@token_role_required()
def save_feedback(current_user):
    # 获取 JSON 数据
    feedback_data = request.get_json()

    # 创建一个新反馈
    save_feedback = Feedback(
        description = feedback_data.get('description'),
        technology = feedback_data.get('technology'),
        creator_id = current_user.id
    )

    # 传了id就更新
    if feedback_data.get('id') is not None:
        update_feedback = Feedback.query.filter_by(is_deleted=False).get(feedback_data.get('id'))
        if update_feedback is None:
            return jsonify({'message': 'Feedback not found'}), 404
        update_feedback.description = save_feedback.description
        update_feedback.technology = save_feedback.technology
    else:    
        # 将反馈添加到数据库
        db.session.add(save_feedback)    
    db.session.commit()

    return jsonify({'message': 'Feedback saved successfully'}), 201


"""
    删除反馈信息
"""
@feedback.route('/delete/<int:feedback_id>', methods=['DELETE'])
@token_role_required("admin")
def delete_feedback(feedback_id):
    # 获取要删除的反馈
    feedback_to_delete = Feedback.query.filter_by(is_deleted=False).get(feedback_id)

    if feedback_to_delete:
        # 逻辑删除，将 is_deleted 设置为 True
        feedback_to_delete.is_deleted = True
        db.session.commit()
        return jsonify({'message': 'Feedback deleted successfully'}), 200
    else:
        return jsonify({'message': 'Feedback not found'}), 404