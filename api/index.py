from flask import Blueprint,jsonify
from decorators.decorators import token_required

index = Blueprint('index',__name__)

@index.route('/')
@token_required
def show(current_user):
    return jsonify('pong!')