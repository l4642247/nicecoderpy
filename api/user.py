from flask import Blueprint, json, jsonify, request, make_response, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models.models import User, db
import jwt, uuid

user = Blueprint('user',__name__)

@user.route('/')
def show():
    return 'user api'

# 用户登录
@user.route('/login', methods =['POST'])
def login():
    auth = request.form
  
    # 参数校验
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    
    # 查询用户
    user = User.query\
        .filter_by(email = auth.get('email'))\
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


# 注册
@user.route('/signup', methods =['POST'])
def signup():
    # 创建一个表单数据的字典
    data = request.form
  
    # 获取参数
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    # 校验当前用户
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        user = User(
            public_id = str(uuid.uuid4()),
            name = name,
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
    
# 注销
@user.route('/logout', methods =['POST'])
def logout():
    # 清除 Flask 的 session 数据
    session.pop('x-access-token', None)
    session.pop('user_id', None)
    return make_response('Successfully logout.', 201)

