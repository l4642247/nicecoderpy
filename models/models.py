from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
    用户
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    phone = db.Column(db.String(20), unique=True) 
    password = db.Column(db.String(200))
    user_type = db.Column(db.String(10), default='customer')  # 'customer' or 'employee'
    balance = db.Column(db.Float, default=0.0)
    position = db.Column(db.String(255))  # Only for employee type
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

"""
    服务
"""
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

"""
    预约
"""
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    appointment_time = db.Column(db.DateTime, nullable=False)
    service = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

"""
    服务记录
"""
class ServiceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    service_time = db.Column(db.DateTime, nullable=False)
    service = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
