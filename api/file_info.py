from flask import Blueprint, jsonify, request
from models.models import FileInfo, db

file_info = Blueprint('file_info', __name__)

@file_info.route('/page', methods=['GET'])
def get_file_info_page():
    page_num = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    file_infos = FileInfo.query.paginate(page=page_num, per_page=per_page, error_out=False)
    
    if file_infos.items:
        file_info_list = [file_info.serialize() for file_info in file_infos.items]
        response_data = {"code": 0, "data": file_info_list, "count": file_infos.total}
        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'No file info found'}), 404

@file_info.route('/create', methods=['POST'])
def create_file_info():
    data = request.json
    file_code = data.get('file_code')
    file_address = data.get('file_address')
    extraction_code = data.get('extraction_code')
    project_id = data.get('project_id')
    
    new_file_info = FileInfo(file_code=file_code, file_address=file_address, extraction_code=extraction_code, project_id=project_id)
    
    db.session.add(new_file_info)
    db.session.commit()
    
    return jsonify({'message': 'File info created successfully'}), 201

@file_info.route('/<int:file_id>', methods=['GET'])
def get_file_info(file_id):
    file_info = FileInfo.query.get(file_id)
    if file_info:
        return jsonify({'file_info': file_info.serialize()}), 200
    else:
        return jsonify({'message': 'File info not found'}), 404

@file_info.route('/<int:file_id>', methods=['PUT'])
def update_file_info(file_id):
    data = request.json
    file_info = FileInfo.query.get(file_id)
    
    if file_info:
        file_info.file_code = data.get('file_code', file_info.file_code)
        file_info.file_address = data.get('file_address', file_info.file_address)
        file_info.extraction_code = data.get('extraction_code', file_info.extraction_code)
        file_info.project_id = data.get('project_id', file_info.project_id)
        
        db.session.commit()
        return jsonify({'message': 'File info updated successfully'}), 200
    else:
        return jsonify({'message': 'File info not found'}), 404

@file_info.route('/<int:file_id>', methods=['DELETE'])
def delete_file_info(file_id):
    file_info = FileInfo.query.get(file_id)
    if file_info:
        db.session.delete(file_info)
        db.session.commit()
        return jsonify({'message': 'File info deleted successfully'}), 200
    else:
        return jsonify({'message': 'File info not found'}), 404
