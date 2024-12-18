from datetime import datetime, timedelta

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Cnm.0001+@121.43.130.247:3306/coding'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 是否追踪数据库修改，一般不开启, 会影响性能
    SQLALCHEMY_ECHO = True # 是否显示底层执行的SQL语句
    
    # redis配置
    REDIS_HOST = '121.43.130.247'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = 'Cnm.0001+'

    # 秘钥
    SECRET_KEY = "nicecoder"

    # JWT超时时间
    JWT_EXPIRATION = datetime.utcnow() + timedelta(hours=1)

    # SESSION
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # 文件上传路径
    UPLOAD_FOLDER = "/app/uploads"

app_config = {
    'development': Config,
    'production': Config,
    'default': Config
}