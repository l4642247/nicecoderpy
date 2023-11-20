import jwt
from functools import wraps
from flask import json, jsonify, request, current_app, session
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from models.models import User

# JWT校验
def token_role_required(role = None):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # 获取token
            if 'x-access-token' in session:
                token = session['x-access-token']

            # token校验不通过，返回401
            if not token:
                return jsonify({'message' : 'Token is missing !!'}), 401
            
            try:
                # 解码负载以获取存储的详细信息
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query\
                    .filter_by(public_id = data['public_id'])\
                    .first()
                if role is not None and current_user.user_type != role:
                    return jsonify({'message' : 'Permission denied !!'}), 403
            except ExpiredSignatureError:
                return jsonify({'message' : 'Token has expired !!'}), 401
            except InvalidTokenError:
                return jsonify({'message' : 'Token is invalid !!'}), 401
            
            # 将当前登录用户的上下文返回给路由
            return f(current_user, *args, **kwargs)
        
        return decorated
    return token_required