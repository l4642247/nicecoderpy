from flask import Blueprint, jsonify, request
from decorators.decorators import token_role_required
from models.models import Appointment, User, db
from datetime import datetime

appointment = Blueprint('appointment',__name__)

# 转换为预约信息的字典
def appointment_to_dict(appointment):
    return {
        'id': appointment.id,
        'customer_id': appointment.customer_id,
        'employee_id': appointment.employee_id,
        'service': appointment.service,
        'notes': appointment.notes,
        'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
        'creation_time': appointment.creation_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
# 增加预约项目
@appointment.route('/save', methods=['POST'])
@token_role_required()
def add_appointment(current_user):
    data = request.get_json()
    
    save_appointment = Appointment(
        customer_id = current_user.id,
        employee_id = data.get('employee_id'),
        appointment_time = datetime.utcnow(),
        service = data.get('service'),
        notes = data.get('notes')
    )
    # 传了id就更新
    if data.get('id') is not None:
        update_appointment = Appointment.query.get(data.get('id'))
        if update_appointment is None:
            return jsonify({'message': 'Appointment not found'}), 404
        update_appointment.customer_id = save_appointment.customer_id
        update_appointment.employee_id = save_appointment.employee_id
        update_appointment.appointment_time = save_appointment.appointment_time
        update_appointment.service = save_appointment.service
        update_appointment.notes = save_appointment.notes
    else:
        # 将预约添加到数据库
        db.session.add(save_appointment)
        
    db.session.commit()
    return jsonify({'message': 'Appointment added successfully'}), 201

# 获取所有预约项目
@appointment.route('/', methods=['GET'])
@appointment.route('/<int:appointment_id>', methods=['GET'])
def get_appointment_by_id(appointment_id=None):
    if appointment_id is not None:
        # 获取单个预约项目
        appointment = Appointment.query.get_or_404(appointment_id)
        return jsonify(appointment_to_dict(appointment))
    else:
        # 获取所有预约项目
        appointments = Appointment.query.all()
        appointment_list = [appointment_to_dict(appointment) for appointment in appointments]
        return jsonify({'appointments': appointment_list})
    
# 获取单用户所有预约项目
@appointment.route('/user/<int:user_id>', methods=['GET'])
def get_appointment_by_user_id(user_id=None):
    if user_id is not None:
        user = User.query.get_or_404(user_id)
        # 获取单用户所有服务项目
        if user.user_type == 'customer':
            appointments = Appointment.query.filter_by(customer_id = user_id).all()
        elif user.user_type == 'employee':
            appointments = Appointment.query.filter_by(employee_id = user_id).all()
        appointment_list = [appointment_to_dict(appointment) for appointment in appointments]
        return jsonify({'appointments': appointment_list})
    else:
        return jsonify({'message': 'user_id cannot be empty'}), 400
    
# 删除预约项目
@appointment.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'})    
