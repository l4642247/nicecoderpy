from flask import Blueprint, jsonify, request
from decorators.decorators import token_role_required
from models.models import ServiceRecord, User, db
from datetime import datetime

service_record = Blueprint('service_record',__name__)

# 转换为服务信息的字典
def service_record_to_dict(record):
    return {
        'id': record.id,
        'service_time': record.service_time.strftime('%Y-%m-%d %H:%M:%S'),
        'customer_id': record.customer_id,
        'employee_id': record.employee_id,
        'service': record.service,
        'amount': record.amount,
        'notes': record.notes,
        'creation_time': record.creation_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
# 增加服务项目
@service_record.route('/save', methods=['POST'])
@token_role_required()
def add_service_record(current_user):
    data = request.get_json()
    
    save_service_record = ServiceRecord(
        service_time = datetime.utcnow(),
        customer_id = data.get('customer_id'),
        employee_id = current_user.id,
        service = data.get('service'),
        amount = data.get('amount'),
        notes = data.get('notes')
    )
    # 传了id就更新
    if data.get('id') is not None:
        update_service_record = ServiceRecord.query.get(data.get('id'))
        if update_service_record is None:
            return jsonify({'message': 'ServiceRecord not found'}), 404
        update_service_record.service_time = save_service_record.service_time
        update_service_record.customer_id = save_service_record.customer_id
        update_service_record.employee_id = save_service_record.employee_id
        update_service_record.service = save_service_record.service
        update_service_record.amount = save_service_record.amount
        update_service_record.notes = save_service_record.notes
    else:
        # 将服务添加到数据库
        db.session.add(save_service_record)

    db.session.commit()
    return jsonify({'message': 'ServiceRecord added successfully'}), 201

# 获取所有服务项目
@service_record.route('/', methods=['GET'])
@service_record.route('/<int:service_record_id>', methods=['GET'])
def get_service_record_by_id(service_record_id=None):
    if service_record_id is not None:
        # 获取单个服务项目
        service_record = ServiceRecord.query.get_or_404(service_record_id)
        return jsonify(service_record_to_dict(service_record))
    else:
        # 获取所有服务项目
        service_records = ServiceRecord.query.all()
        service_record_list = [service_record_to_dict(service_record) for service_record in service_records]
        return jsonify({'service_records': service_record_list})
    
# 获取单用户所有服务项目
@service_record.route('/user/<int:user_id>', methods=['GET'])
def get_service_record_by_user_id(user_id=None):
    if user_id is not None:
        user = User.query.get_or_404(user_id)
        # 获取单用户所有服务项目
        if user.user_type == 'customer':
            service_records = ServiceRecord.query.filter_by(customer_id = user_id).all()
        elif user.user_type == 'employee':
            service_records = ServiceRecord.query.filter_by(employee_id = user_id).all()
        service_record_list = [service_record_to_dict(service_record) for service_record in service_records]
        return jsonify({'service_records': service_record_list})
    else:
        return jsonify({'message': 'user_id cannot be empty'}), 400
    
# 删除服务项目
@service_record.route('/<int:service_record_id>', methods=['DELETE'])
def delete_service_record(service_record_id):
    service_record = ServiceRecord.query.get_or_404(service_record_id)
    db.session.delete(service_record)
    db.session.commit()
    return jsonify({'message': 'ServiceRecord deleted successfully'})    
