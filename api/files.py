from flask import Flask, send_from_directory, request, current_app, Blueprint, jsonify, send_file
from werkzeug.utils import secure_filename
import os, shutil, uuid, zipfile, threading, posixpath
from datetime import datetime

files = Blueprint('files', __name__)

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

# 假设 create_upload_folder 函数已经定义，用于创建上传目录
def create_upload_folder():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

@files.route('/upload', methods=['POST'])
def upload_file():
    create_upload_folder()  # 确保上传目录存在

    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]  # 获取文件扩展名
        # 获取当前日期，格式为 YYYY-MM-DD
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        date_folder = posixpath.join(current_app.config['UPLOAD_FOLDER'], current_date)
        # 创建日期文件夹（如果不存在）
        os.makedirs(date_folder, exist_ok=True)
        # 生成唯一的文件名，避免文件名冲突
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = posixpath.join(date_folder, unique_filename)
        # 保存文件
        file.save(file_path)
        # 生成文件的 URL（根据实际情况修改）
        file_url = get_file_url(posixpath.join(current_date, unique_filename))

        return jsonify({
            'message': 'File uploaded successfully',
            'file_url': file_url
        })

def get_file_url(file_path):
    # 这里需要根据您的应用配置生成文件的URL
    # 例如，如果您的应用运行在 http://example.com，并且上传目录是 /static/uploads
    # 您可以这样生成URL：
    # return f"http://example.com/static/uploads/{file_path}"
    # 这里假设 get_file_url 函数已经实现
    return f"http://121.43.130.247/uploads/{file_path}"

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

    
