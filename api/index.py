from flask import Blueprint,request,render_template,current_app,redirect,session,jsonify
from models.redis_client import RedisClient
from decorators.decorators import token_role_required
from models.models import User, db
index = Blueprint('index',__name__)

@index.route('/')
def home():
    return render_template('home.html')

@index.route('/admin')
# @token_role_required(role='admin')
def admin():
    return render_template('admin/index.html')

@index.route('/admin/user')
# @token_role_required(role='admin')
def user():
    return render_template('admin/user.html')

@index.route('/admin/user/page')
# @token_role_required(role='admin')
def userPage():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    serialized_users = [user.serialize() for user in users.items]
    response_data = {"code": 0, "data": serialized_users}
    return jsonify(response_data)


