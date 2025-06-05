# 使用官方 Python 3.11 的精简镜像
FROM python:3.11-slim

# 环境变量设置
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖，支持 cryptography、Pillow、minio 等编译
RUN apt-get update && apt-get install -y \
  build-essential \
  libmariadb-dev-compat \
  libmariadb-dev \
  libjpeg-dev \
  zlib1g-dev \
  libffi-dev \
  libssl-dev \
  python3-dev \
  git \
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 拷贝 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# 拷贝项目源代码
COPY . .

# 端口暴露
EXPOSE 8000

# 启动命令
CMD ["daphne", "config.asgi:application", "--port", "8000", "--bind", "0.0.0.0"]
