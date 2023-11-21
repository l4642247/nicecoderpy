from flask import Blueprint, json, jsonify, request, make_response, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from decorators.decorators import token_role_required
from datetime import datetime, timedelta
from models.models import User, db
import jwt, uuid

user = Blueprint('user',__name__)

# 注册
@user.route('/signup', methods =['POST'])
def signup():
    # 创建一个表单数据的字典
    data = request.form
  
    # 获取参数
    name, phone, email= data.get('name'), data.get('phone'), data.get('email')
    password = data.get('password',"123456")

    # 校验入参
    if 'phone' not in data or not data['phone']:
        return jsonify({'message': 'Phone number cannot be empty'}), 400
  
    # 校验当前用户
    user = User.query\
        .filter_by(phone = phone)\
        .first()
    if not user:
        user = User(
            public_id = str(uuid.uuid4()),
            name = name,
            phone = phone,
            email = email,
            password = generate_password_hash(password)
        )
        # 插入数据
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # 用户已存在返回202
        return make_response('User already exists. Please Log in.', 202)
    
# 用户登录
@user.route('/login', methods =['POST'])
def login():
    auth = request.form
  
    # 参数校验
    if not auth or not auth.get('phone') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    
    # 查询用户
    user = User.query\
        .filter_by(phone = auth.get('phone'))\
        .first()
  
    if not user:
        # 返回401，用户不存在
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        # 构造头部
        header = {
            'alg': 'HS256',  # 使用 HMAC SHA-256 算法进行签名
            'typ': 'JWT'
        }
        
        # 生成JWT
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : current_app.config['JWT_EXPIRATION']
        }, current_app.config['SECRET_KEY'], algorithm='HS256', headers=header)

        # 存入session
        session["x-access-token"] = token
        session["user_id"] = user.public_id

        return make_response(jsonify({'token' : token}), 201)

    # 密码错误返回403
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

@user.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_name, new_phone, new_email= request.form.get('name'), request.form.get('phone'), request.form.get('email')
    new_balance = request.form.get('balance')

    # 更新用户信息
    if new_name:
        user.name = new_name
    if new_email:
        user.email = new_email
    if new_phone:
        user.phone = new_phone
    if new_balance:
        user.balance = new_balance

    # 保存更新到数据库
    db.session.commit()

    return jsonify({'message': 'User updated successfully'})

# 修改密码
@user.route('/change_password', methods=['POST'])
@token_role_required()  # 保证用户已登录
def change_password(current_user):
    user = current_user

    # 获取旧密码和新密码
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    # 验证旧密码
    if not check_password_hash(user.password, old_password):
        return jsonify({'error': 'Invalid old password'}), 400

    # 更新密码
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200
    
# 注销
@user.route('/logout', methods =['POST'])
def logout():
    # 清除 Flask 的 session 数据
    session.pop('x-access-token', None)
    session.pop('user_id', None)
    return make_response('Successfully logout.', 201)

# 删除服务项目
@user.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})    


