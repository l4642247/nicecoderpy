from flask import Flask
from api.index import index
from api.user import user
from api.service import service
from api.service_record import service_record
from api.appointment import appointment
from flask_cors import CORS

from models.models import db
from config.config import app_config
import os

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(index,url_prefix='/')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(service,url_prefix='/service')
app.register_blueprint(service_record,url_prefix='/service_record')
app.register_blueprint(appointment,url_prefix='/appointment')

env = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(app_config[env])

# 初始化数据库
db.init_app(app)

# 创建所有定义的数据库表
with app.app_context():
    db.create_all()

# 允许跨域
CORS(app, resources={r'/*': {'origins': '*'}})

if __name__=='__main__':
  app.run()