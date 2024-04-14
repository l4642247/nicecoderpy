from flask import Blueprint,render_template
from models.redis_client import RedisClient
index = Blueprint('index',__name__)

@index.route('/')
def home():
    return render_template('home.html')