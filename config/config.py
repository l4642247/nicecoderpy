class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/testdb'
    # 是否追踪数据库修改，一般不开启, 会影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示底层执行的SQL语句
    SQLALCHEMY_ECHO = True

    # 用户密码加密
    SECRET_KEY = "nicecoder"

app_config = {
    'development': Config,
    'production': Config,
    'default': Config
}