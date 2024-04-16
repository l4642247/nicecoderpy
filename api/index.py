from flask import Blueprint,render_template,current_app,redirect,session
from models.redis_client import RedisClient
index = Blueprint('index',__name__)

@index.route('/')
def home():
    return render_template('home.html')

@index.route('/admin')
def test():
    return render_template('admin/login.html')


