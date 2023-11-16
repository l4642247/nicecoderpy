import jwt
from functools import wraps
from flask import json, jsonify, request, current_app
from models.models import User

# JWT校验
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # 获取token
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # token校验不通过，返回401
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # 解码负载以获取存储的详细信息
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
            if current_user.role != 'admin':
                return jsonify({'message' : 'Permission denied !!'}), 403
        except:
            return jsonify({'message' : 'Token is invalid !!'}), 401
        # 将当前登录用户的上下文返回给路由
        return  f(current_user, *args, **kwargs)
    return decorated