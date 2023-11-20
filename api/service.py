from flask import Blueprint, jsonify, request
from decorators.decorators import token_role_required
from models.models import Service, db

service = Blueprint('service',__name__)

# 转换为服务信息的字典
def service_to_dict(service):
    return {
        'id': service.id,
        'name': service.name,
        'price': service.price,
        'description': service.description,
        'creation_time': service.creation_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
# 增加服务项目
@service.route('/save', methods=['POST'])
def add_service():
    data = request.get_json()
    
    save_service = Service(
        name=data.get('name'),
        price=data.get('price'),
        description=data.get('description')
    )
    # 传了id就更新
    if data.get('id') is not None:
        update_service = Service.query.get(data.get('id'))
        print(data.get('id'))
        if update_service is None:
            return jsonify({'message': 'Service not found'}), 404
        update_service.name = save_service.name
        update_service.price = save_service.price
        update_service.description = save_service.description
    else:
        # 将服务添加到数据库
        db.session.add(save_service)

    db.session.commit()
    return jsonify({'message': 'Service added successfully'}), 201    

# 获取所有服务项目
@service.route('/', methods=['GET'])
@service.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id=None):
    if service_id is not None:
        # 获取单个服务项目
        service = Service.query.get_or_404(service_id)
        return jsonify(service_to_dict(service))
    else:
        # 获取所有服务项目
        services = Service.query.all()
        service_list = [service_to_dict(service) for service in services]
        return jsonify({'services': service_list})
    
# 删除服务项目
@service.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'})    
