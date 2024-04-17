from flask import Blueprint,render_template,current_app,redirect,session
from models.redis_client import RedisClient
from decorators.decorators import token_role_required
index = Blueprint('index',__name__)

@index.route('/')
def home():
    return render_template('home.html')

@index.route('/admin')
# @token_role_required(role='admin')
def admin():
    return render_template('admin/index.html')


