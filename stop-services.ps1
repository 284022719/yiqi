# 停止一起公会网站服务脚本 (Windows PowerShell)

Write-Host "🛑 停止一起公会网站服务..." -ForegroundColor Yellow

# 停止后端服务
Write-Host "🐍 停止后端服务..." -ForegroundColor Yellow
$backendProcesses = Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*uvicorn*"}
if ($backendProcesses) {
    $backendProcesses | Stop-Process -Force
    Write-Host "✅ 后端服务已停止" -ForegroundColor Green
} else {
    Write-Host "ℹ️ 未找到运行中的后端服务" -ForegroundColor Gray
}

# 停止前端服务
Write-Host "⚛️ 停止前端服务..." -ForegroundColor Yellow
$frontendProcesses = Get-Process | Where-Object {$_.ProcessName -like "*node*" -and $_.CommandLine -like "*serve*"}
if ($frontendProcesses) {
    $frontendProcesses | Stop-Process -Force
    Write-Host "✅ 前端服务已停止" -ForegroundColor Green
} else {
    Write-Host "ℹ️ 未找到运行中的前端服务" -ForegroundColor Gray
}

# 检查端口占用
Write-Host "🔍 检查端口占用..." -ForegroundColor Yellow
$port8000 = netstat -ano | findstr :8000
$port3000 = netstat -ano | findstr :3000

if ($port8000) {
    Write-Host "⚠️ 端口8000仍被占用: $port8000" -ForegroundColor Red
} else {
    Write-Host "✅ 端口8000已释放" -ForegroundColor Green
}

if ($port3000) {
    Write-Host "⚠️ 端口3000仍被占用: $port3000" -ForegroundColor Red
} else {
    Write-Host "✅ 端口3000已释放" -ForegroundColor Green
}

Write-Host "✅ 服务停止完成！" -ForegroundColor Green 