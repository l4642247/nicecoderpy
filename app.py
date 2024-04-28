from flask import Flask
from api.index import index
from api.user import user
from api.project import project
from api.feedback import feedback
from api.wechat import wechat
from api.files import files
from api.file_info import file_info

from flask_cors import CORS
from models.models import db
from config.config import app_config
import os

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(index,url_prefix='/')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(project,url_prefix='/project')
app.register_blueprint(feedback,url_prefix='/feedback')
app.register_blueprint(wechat,url_prefix='/wechat')
app.register_blueprint(files,url_prefix='/files')
app.register_blueprint(file_info,url_prefix='/file_info')


# 会话支持
app.secret_key = 'one'

# 环境
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