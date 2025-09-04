#!/bin/bash

echo "🚀 启动 CFMP Kubernetes 应用..."

# 启动 minikube


# 配置 Docker 环境


# 构建镜像
echo "构建后端镜像..."
cd 后端/cfmp && docker build -t backend . && cd ../..

echo "docker镜像存储"
docker save backend > images.tar

echo "导入镜像"
k3s ctr images import images.tar
rm images.tar
# 部署应用
echo "部署应用..."
k3s kubectl delete -f k8s/ --ignore-not-found=true
sleep 3

# 等待数据库服务就绪
sleep 5

k3s kubectl  apply -f k8s/

# 等待启动
echo "等待应用启动..."
k3s kubectl  wait --for=condition=ready pod -l io.kompose.service=backend --timeout=300s
k3s kubectl  wait --for=condition=ready pod -l io.kompose.service=frontend --timeout=300s

# 暴露服务

# 显示访问地址
echo ""
echo "✅ 部署完成！访问地址："
k3s service list | grep -E "(frontend|backend)"
echo ""
echo "前端: $(k3s service frontend --url)"
echo "后端: $(k3s service backend --url)"
