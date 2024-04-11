from flask import Blueprint,jsonify
from decorators.decorators import token_role_required
from models.models import User

index = Blueprint('index',__name__)

@index.route('/')
def show():
    return jsonify({'message': 'Deployment successful!'})