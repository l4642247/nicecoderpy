from flask import Blueprint,jsonify
from decorators.decorators import token_role_required
from models.models import User

index = Blueprint('index',__name__)

@index.route('/')
@token_role_required()
def show(current_user):
    users = User.query.all()

    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        user_list.append(user_data)

    return jsonify({'users': user_list})