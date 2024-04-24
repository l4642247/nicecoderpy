from flask import Flask, send_from_directory, request, current_app, Blueprint, jsonify, send_file
from werkzeug.utils import secure_filename
import os, shutil, uuid, zipfile, threading, datetime

files = Blueprint('files', __name__)

def get_file_url(filename):
    return f"http://localhost/files/{filename}"

def create_upload_folder():
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])

@files.route('/<path:filename>')
def download_file(filename):
    directory = current_app.config['UPLOAD_FOLDER']
    full_path = os.path.join(directory, filename)
    if os.path.exists(full_path):
        # 获取文件后缀
        _, file_extension = os.path.splitext(filename)
        return send_file(full_path, mimetype='application/octet-stream', as_attachment=True, download_name=f"{filename}")
    else:
        return 'File not found', 404

@files.route('/upload', methods=['POST'])
def upload_file():
    create_upload_folder()  # 确保上传目录存在
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        # 生成唯一的文件名，避免文件名冲突
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
        file_url = get_file_url(unique_filename)
        return jsonify({'message': 'File uploaded successfully', 'file_url': file_url})

@files.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return 'File deleted successfully'
    else:
        return 'File not found'

@files.route('/delete/all', methods=['DELETE'])
def backup_and_delete_files():
    folder = current_app.config['UPLOAD_FOLDER']
    if os.path.exists(folder):
        def backup_and_delete():
            # 获取当前时间作为备份文件名的一部分
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # 创建备份 zip 文件
            backup_file = os.path.join(os.path.dirname(folder), f'backup_{current_time}.zip')
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, folder))

            # 清空文件夹
            for root, dirs, files in os.walk(folder):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))

        # 在后台线程中执行备份和清空操作
        backup_thread = threading.Thread(target=backup_and_delete)
        backup_thread.start()

        return 'Backup process started successfully'
    else:
        return 'Folder not found'

    
