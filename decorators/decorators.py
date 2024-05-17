import jwt
from functools import wraps
from flask import jsonify, request, current_app
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from models.models import User

# 辅助函数：生成错误响应
def error_response(message, status_code):
    response = jsonify({'message': message})
    response.status_code = status_code
    return response

# 校验是否登录
def token_required():
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('x-access-token')
            # 检查是否存在token
            if not token:
                return error_response('Token is missing !!', 401)
            
            try:
                # 解码负载以获取存储的详细信息
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            except ExpiredSignatureError:
                return error_response('Token has expired !!', 401)
            except InvalidTokenError:
                return error_response('Token is invalid !!', 401)
            
            # 将当前登录用户的上下文返回给路由
            return f(*args, **kwargs)
        return decorated
    return token_required

# 校验角色并获取用户
def token_role_required(role=None):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('x-access-token')
            
            # 检查是否存在token
            if not token:
                return error_response('Token is missing !!', 401)
            try:
                # 解码负载以获取存储的详细信息
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
                # 检查角色权限
                if role is not None and current_user.role != role:
                    return error_response('Permission denied !!', 403)
            except ExpiredSignatureError:
                return error_response('Token has expired !!', 401)
            except InvalidTokenError:
                return error_response('Token is invalid !!', 401)
            
            # 将当前登录用户的上下文返回给路由
            return f(current_user, *args, **kwargs)
        return decorated
    return token_required


