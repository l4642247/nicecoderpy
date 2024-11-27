from flask import Flask, send_from_directory, request, current_app, Blueprint, jsonify, send_file
from werkzeug.utils import secure_filename
import os, io, shutil, uuid, zipfile, threading, posixpath
from datetime import datetime
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# 创建一个全局的线程池
executor = ThreadPoolExecutor(max_workers=5)

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
        
def custom_secure_filename(filename):
    # 提取文件扩展名
    ext = os.path.splitext(filename)[1]
    # 保留中文及常规字符
    base = ''.join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-'))
    # 返回文件名，去掉不合法字符并保留原扩展名
    return base.strip().rsplit('.', 1)[0] + ext

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_image(file_path, max_size_mb=5, quality_step=5, min_quality=30):
    """
    异步压缩图片到指定大小以下，同时尽量保持图片质量。

    :param file_path: 图片路径
    :param max_size_mb: 目标最大大小（MB）
    :param quality_step: 每次调整质量的步长
    :param min_quality: 最低质量阈值
    """
    def do_compress():
        try:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if size_mb <= max_size_mb:
                # 如果文件已经小于等于目标大小，则不需要压缩
                return

            # 打开图片
            with Image.open(file_path) as img:
                img_format = img.format
                img = img.convert('RGB')  # 转换为RGB模式，避免某些模式导致的问题

                # 初始质量设置
                quality = 95

                while quality >= min_quality:
                    # 将图片保存到内存中的字节流
                    buffer = io.BytesIO()
                    img.save(buffer, format=img_format, quality=quality)
                    buffer.seek(0)
                    size = buffer.getbuffer().nbytes / (1024 * 1024)

                    if size <= max_size_mb:
                        # 如果满足大小要求，则将压缩后的图片写入临时文件
                        temp_file_path = f"{file_path}.tmp"
                        with open(temp_file_path, 'wb') as f_out:
                            f_out.write(buffer.getvalue())
                        break
                    else:
                        quality -= quality_step

                # 如果降低到最低质量仍大于目标大小，则保存最低质量的图片
                if quality < min_quality:
                    with open(file_path, 'wb') as f_out:
                        img.save(f_out, format=img_format, quality=quality)

            # 替换原始文件
            os.replace(file_path + '.tmp', file_path)
        except Exception as e:
            current_app.logger.error(f'Error compressing image {file_path}: {e}')

    executor.submit(do_compress)


@files.route('/upload', methods=['POST'])
def upload_file():
    create_upload_folder()  # 确保上传目录存在

    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    # 检查文件扩展名
    if not allowed_file(file.filename):
        return jsonify({"error": "Only image files (jpg, jpeg, png, gif) are allowed"}), 400

    if file:
        filename = custom_secure_filename(file.filename)
        current_app.logger.info(f'filename: {filename}')
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
        
         # 压缩图片
        compress_image(file_path)

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
    return f"http://121.43.130.247/images/{file_path}"

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

    
