from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    public_id = db.Column(db.String(50), unique = True)
    openid = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(10), default = 'user')
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    last_api_call_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.Integer)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = db.Column(db.Boolean, default=False)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    technology = db.Column(db.String(255))
    approval_status = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.Integer)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = db.Column(db.Boolean, default=False)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL(10, 2))
    payment_status = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.Integer)    
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = db.Column(db.Boolean, default=False)
    
class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(255), nullable=False)
    received_message = db.Column(db.Text, nullable=False)
    reply_message = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=True, default=db.func.current_timestamp())
