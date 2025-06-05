# 使用官方 Node 镜像
FROM node:24-alpine

# 设置工作目录
WORKDIR /app

# 设置Docker环境变量
ENV DOCKER_ENV=true

# 复制 package.json 和 lock 文件
COPY package.json package-lock.json* ./

# 安装依赖
RUN npm install

# 复制项目所有文件
COPY . .

# 暴露端口
EXPOSE 80

# 启动开发服务器
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "80"]
