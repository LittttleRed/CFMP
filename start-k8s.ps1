#!/usr/bin/env pwsh

Write-Host "🚀 启动 CFMP Kubernetes 应用..." -ForegroundColor Green

# 启动 minikube
Write-Host "启动 minikube..." -ForegroundColor Yellow
minikube start
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ minikube 启动失败" -ForegroundColor Red
    exit 1
}

# 配置 Docker 环境
Write-Host "配置 Docker 环境..." -ForegroundColor Yellow
$dockerEnv = minikube docker-env --shell powershell
if ($dockerEnv) {
    Invoke-Expression $dockerEnv
}

# 构建镜像
Write-Host "构建后端镜像..." -ForegroundColor Yellow
Push-Location "后端/cfmp"
docker build -t backend .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 后端镜像构建失败" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

Write-Host "构建前端镜像..." -ForegroundColor Yellow
Push-Location "前端/cfmp-front-end"
docker build -t frontend .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 前端镜像构建失败" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# 部署应用
Write-Host "部署应用..." -ForegroundColor Yellow
kubectl delete -f k8s/ --ignore-not-found=true
Start-Sleep -Seconds 3
kubectl create -f k8s/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 应用部署失败" -ForegroundColor Red
    exit 1
}

# 等待启动
Write-Host "等待应用启动..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l io.kompose.service=backend --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 后端服务启动超时" -ForegroundColor Red
    exit 1
}

kubectl wait --for=condition=ready pod -l io.kompose.service=frontend --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 前端服务启动超时" -ForegroundColor Red
    exit 1
}

# 暴露服务
Write-Host "暴露服务..." -ForegroundColor Yellow
kubectl patch service frontend -p '{"spec":{"type":"NodePort"}}'
kubectl patch service backend -p '{"spec":{"type":"NodePort"}}'

# 显示访问地址
Write-Host ""
Write-Host "✅ 部署完成！访问地址：" -ForegroundColor Green

# 获取服务列表
$services = kubectl get services -o json | ConvertFrom-Json
$frontendService = $services.items | Where-Object { $_.metadata.name -eq "frontend" }
$backendService = $services.items | Where-Object { $_.metadata.name -eq "backend" }

if ($frontendService -and $backendService) {
    minikube service list | Select-String -Pattern "(frontend|backend)"
    Write-Host ""
    
    # 获取服务URL
    $frontendUrl = minikube service frontend --url
    $backendUrl = minikube service backend --url
    
    Write-Host "前端: $frontendUrl" -ForegroundColor Cyan
    Write-Host "后端: $backendUrl" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  服务信息获取失败，请手动检查服务状态" -ForegroundColor Yellow
    kubectl get services
}

Write-Host ""
Write-Host "🎉 CFMP 应用已成功启动！" -ForegroundColor Green
