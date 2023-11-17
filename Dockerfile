# 使用官方 Python 镜像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用程序端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 运行应用程序
CMD ["flask", "run"]
