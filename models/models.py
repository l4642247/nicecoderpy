from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(50), unique=True)
    openid = Column(String(100), unique=True)
    name = Column(String(100))
    email = Column(String(70), unique=True)
    password = Column(String(200))
    role = Column(String(10), default='user')
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    last_api_call_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())

    def serialize(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'openid': self.openid,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_api_call_time': self.last_api_call_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
class Product(db.Model):
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # 商品名称
    description = Column(Text, nullable=True)   # 商品描述
    price = Column(Float, nullable=False)       # 商品价格
    stock = Column(Integer, default=0)          # 库存数量
    category = Column(String(100), nullable=False)  # 商品类别
    image_url = Column(String(255), nullable=True)  # 商品图片 URL
    status = Column(Boolean, default=True)      # 是否上架
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())  # 创建时间
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, default=False) # 是否已删除

    def serialize(self):
        """将商品对象序列化为字典"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'image_url': self.image_url,
            'status': self.status,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }
        
class Shipment(db.Model):
    shipment_id = Column(Integer, primary_key=True, autoincrement=True)  # 发货 ID
    order_id = Column(Integer, nullable=False)                           # 订单 ID
    tracking_number = Column(String(255), nullable=False, unique=True)   # 追踪单号
    carrier = Column(String(100), nullable=False)                        # 承运商名称
    status = Column(String(50), default='pending')                       # 发货状态（如 pending、shipped、delivered）
    shipped_date = Column(TIMESTAMP, nullable=True)                      # 发货日期
    delivery_date = Column(TIMESTAMP, nullable=True)                     # 预计送达日期
    recipient_name = Column(String(255), nullable=False)                 # 收件人姓名
    recipient_address = Column(Text, nullable=False)                     # 收件人地址
    recipient_phone = Column(String(20), nullable=False)                 # 收件人电话
    is_delivered = Column(Boolean, default=False)                        # 是否已送达
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())  # 记录创建时间
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, default=False) # 是否已删除

    def serialize(self):
        """将发货对象序列化为字典"""
        return {
            'shipment_id': self.shipment_id,
            'order_id': self.order_id,
            'tracking_number': self.tracking_number,
            'carrier': self.carrier,
            'status': self.status,
            'shipped_date': self.shipped_date.strftime('%Y-%m-%d %H:%M:%S') if self.shipped_date else None,
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d %H:%M:%S') if self.delivery_date else None,
            'recipient_name': self.recipient_name,
            'recipient_address': self.recipient_address,
            'recipient_phone': self.recipient_phone,
            'is_delivered': self.is_delivered,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }

class Project(db.Model):
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    content = Column(Text)
    thumbnail_url = Column(String(255))
    status = Column(Integer, default=0)
    creator_id = Column(Integer)
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, default=False)

    def serialize(self):
        return {
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'thumbnail_url': self.thumbnail_url,
            'status': self.status,
            'creator_id': self.creator_id,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }

class Comment(db.Model):
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    content = Column(Text)
    creator_id = Column(Integer)
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, default=False)

    def serialize(self):
        return {
            'comment_id': self.comment_id,
            'project_id': self.project_id,
            'content': self.content,
            'creator_id': self.creator_id,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }

class Feedback(db.Model):
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    technology = Column(String(255))
    approval_status = Column(Integer, default=0)
    creator_id = Column(Integer)
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, default=False)

    def serialize(self):
        return {
            'feedback_id': self.feedback_id,
            'description': self.description,
            'technology': self.technology,
            'approval_status': self.approval_status,
            'creator_id': self.creator_id,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }

class Order(db.Model):
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer)
    amount = Column(db.DECIMAL(10, 2))
    payment_status = Column(Integer, default=0)
    creator_id = Column(Integer)
    creation_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, default=False)

    def serialize(self):
        return {
            'order_id': self.order_id,
            'project_id': self.project_id,
            'amount': float(self.amount),  # Convert Decimal to float
            'payment_status': self.payment_status,
            'creator_id': self.creator_id,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }

class MessageLog(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(255), nullable=False)
    received_message = Column(Text, nullable=False)
    reply_message = Column(Text, nullable=False)
    create_time = Column(TIMESTAMP, nullable=True, server_default=db.func.current_timestamp())

    def serialize(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'received_message': self.received_message,
            'reply_message': self.reply_message,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }

class FileInfo(db.Model):
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_code = Column(String(10), nullable=False)
    file_address = Column(String(255), nullable=False)
    extraction_code = Column(String(10))
    project_id = Column(Integer)
    download_count = Column(Integer, default=0)
    create_time = Column(TIMESTAMP, nullable=True, server_default=db.func.current_timestamp())
    update_time = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    is_deleted = Column(Boolean, nullable=True)

    def serialize(self):
        return {
            'file_id': self.file_id,
            'file_code': self.file_code,
            'file_address': self.file_address,
            'extraction_code': self.extraction_code,
            'project_id': self.project_id,
            'download_count': self.download_count,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }
