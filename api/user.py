from flask import Blueprint, json, jsonify, request, make_response, current_app, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from decorators.decorators import token_role_required
from datetime import datetime, timedelta
from models.models import User, db
from models.redis_client import RedisClient
import jwt, uuid, random, string

user = Blueprint('user',__name__)


def random_numbers(length):
    return ''.join(random.choices(string.digits, k=length))


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@user.route('/tologin', methods =['GET'])
def tologin():
    redis_client = RedisClient() # 在视图函数中初始化
    code = "LT" + random_numbers(4)
    while redis_client.exists(f"ticket-{code}"):
        code = "LT" + random_numbers(4)
    ticket = random_string(32)
    
    # 5分钟后过期
    redis_client.set(f"ticket-{code}", ticket, ex=5 * 60)
    
    # 返回数据
    return render_template('login.html', code=code, ticket=ticket)

@user.route('/login-check', methods =['GET'])
def login_check_wx():
    redis_client = RedisClient() # 在视图函数中初始化
    code = request.args.get('code')
    ticket = request.args.get('ticket')

    # 校验逻辑
    if not redis_client.exists("Info-" + code):
        return jsonify({"message": "用户未登录"}), 400

    ticket_bak = redis_client.get("ticket-" + code).decode("utf-8")
    if ticket_bak != ticket:
        return jsonify({"message": "登录失败"}), 400

    user_json = redis_client.get("Info-" + code).decode("utf-8")
    user_dict = json.loads(user_json)
    session['current'] = user_dict

    return jsonify({"code": 0,"message": "登录成功"})

# 微信扫码登录
def login_handler(openid, content):
    redis_client = RedisClient()
    # 1、校验content的合法性
    if len(content) != 6 or not redis_client.exists(f"ticket-{content}"):
        return "登录验证码过期或不正确"

    # 2、用户注册处理
    user_dto = register(openid)

    # 3、信息保存到redis中，用于用户登录成功
    user_dict = User.serialize(user_dto)
    redis_client.set(f"Info-{content}", json.dumps(user_dict), ex=5 * 60)

    token = str(uuid.uuid4())
    domain = "http://121.43.130.247/"
    url = f"{domain}/user/autologin?token={token}"

    redis_client.set(f"autologin-{token}", json.dumps(user_dict), ex=48*60*60)

    return f"欢迎你！\n\n<a href='{url}'>点击这里完成登录</a>"


# 注册
def register(openid):
    assert openid is not None, "不合法注册条件"

    user = User.query.filter_by(openid=openid).first()

    if user is None:
        user = User()
        user.name = "User-" + random_string(5)
        user.creation_time = datetime.now()
        user.openid = openid
    else:
        user.last_api_call_time = datetime.now()

    # 插入数据
    db.session.add(user)
    db.session.commit()
    
    return user


@user.route('/autologin', methods=['GET'])
def autologin():
    token = request.args.get('token')
    redis_client = RedisClient() # 在视图函数中初始化
    user_obj = redis_client.get(f"autologin-{token}")

    if user_obj:
        # 假设UserDto是一个字典，这里我们直接使用json.loads来解析
        user_dto = json.loads(user_obj.decode('utf-8'))
        # 在Flask中，你可以使用session来存储用户信息
        session['current'] = user_dto
        return redirect('/')

    return redirect('/login')
    
    
# 用户登录
@user.route('/login', methods =['POST'])
def login_check_pc():
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
