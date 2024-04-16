from flask import Blueprint,render_template,current_app,redirect,session
from models.redis_client import RedisClient
index = Blueprint('index',__name__)

@index.route('/')
def home():
    return render_template('home.html')

@index.route('/test')
def test():
    # 用于前端取值
    session["user_info"] = {'user_id': 123, 'name': 'name'}

    # 打印session的值
    current_app.logger.info(f"Session: {session}")
    return redirect('/')


