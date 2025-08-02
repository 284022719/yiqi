 # 🌐 域名配置指南

## 📋 概述

本文档介绍如何为易骑公会网站配置自定义域名和SSL证书。

## 🎯 配置选项

### 1. 开发环境配置（推荐用于测试）

**特点**:
- 使用自签名SSL证书
- 支持localhost和自定义域名
- 快速部署，无需外部验证

**适用场景**:
- 本地开发测试
- 内网部署
- 功能验证

### 2. 生产环境配置（推荐用于正式部署）

**特点**:
- 使用Let's Encrypt免费SSL证书
- 支持HTTPS加密
- 完整的域名配置

**适用场景**:
- 正式生产环境
- 公网访问
- 需要SSL证书

## 🚀 快速配置

### 使用脚本配置（推荐）

```powershell
# 开发环境配置
.\scripts\configure-domain.ps1 -DomainName "your-domain.com" -UseLetsEncrypt:$false

# 生产环境配置
.\scripts\configure-domain.ps1 -DomainName "your-domain.com" -Email "admin@your-domain.com" -UseLetsEncrypt -Production
```

### 手动配置

#### 1. 更新Nginx配置

编辑 `nginx/nginx.conf` 文件，将 `your-domain.com` 替换为您的实际域名：

```nginx
server {
    listen 443 ssl http2;
    server_name your-actual-domain.com www.your-actual-domain.com;
    # ... 其他配置
}
```

#### 2. 生成SSL证书

**自签名证书（开发环境）**:
```bash
# 生成私钥
openssl genrsa -out nginx/ssl/key.pem 2048

# 生成证书
openssl req -new -x509 -key nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365
```

**Let's Encrypt证书（生产环境）**:
```bash
# 安装certbot
pip install certbot

# 获取证书
certbot certonly --webroot -w /var/www/html -d your-domain.com -d www.your-domain.com

# 复制证书到nginx目录
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
```

#### 3. 更新环境变量

**前端环境变量** (`frontend-refactor/.env.production`):
```env
VITE_API_BASE_URL=https://your-domain.com/api
VITE_APP_NAME=易骑公会官方网站
VITE_APP_VERSION=3.0.0
```

**后端环境变量** (`backend-refactor/.env.production`):
```env
DATABASE_URL=sqlite:///./data/guild_members.db
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
```

## 🔧 DNS配置

### 域名解析设置

在您的域名注册商或DNS服务商处添加以下记录：

**A记录**:
```
your-domain.com     -> 您的服务器IP
www.your-domain.com -> 您的服务器IP
```

**CNAME记录**（可选）:
```
api.your-domain.com -> your-domain.com
```

### 常见DNS服务商配置

**阿里云**:
1. 登录阿里云控制台
2. 进入域名管理
3. 点击"解析设置"
4. 添加A记录

**腾讯云**:
1. 登录腾讯云控制台
2. 进入域名管理
3. 点击"解析"
4. 添加A记录

**Cloudflare**:
1. 登录Cloudflare控制台
2. 选择域名
3. 进入DNS设置
4. 添加A记录

## 🔐 SSL证书管理

### Let's Encrypt证书续期

Let's Encrypt证书有效期为90天，需要定期续期：

```bash
# 手动续期
certbot renew

# 设置自动续期（推荐）
# 添加到crontab
0 12 * * * /usr/bin/certbot renew --quiet
```

### 证书状态检查

```bash
# 检查证书有效期
openssl x509 -in nginx/ssl/cert.pem -text -noout | grep "Not After"

# 检查证书域名
openssl x509 -in nginx/ssl/cert.pem -text -noout | grep "DNS:"
```

## 🚀 部署命令

### 开发环境
```bash
docker-compose -f docker-compose.simple.yml up -d --build
```

### 生产环境
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🔍 验证配置

### 1. 检查服务状态
```bash
# 检查容器状态
docker-compose ps

# 检查Nginx配置
docker exec yiqi-nginx nginx -t
```

### 2. 测试域名访问
```bash
# 测试HTTP重定向
curl -I http://your-domain.com

# 测试HTTPS访问
curl -I https://your-domain.com

# 测试API接口
curl https://your-domain.com/api/health
```

### 3. 检查SSL证书
```bash
# 检查证书信息
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

## 🚨 常见问题

### 1. 域名无法访问
**可能原因**:
- DNS解析未生效
- 防火墙阻止访问
- 服务器端口未开放

**解决方案**:
```bash
# 检查DNS解析
nslookup your-domain.com

# 检查端口开放
telnet your-domain.com 80
telnet your-domain.com 443

# 检查防火墙
sudo ufw status
```

### 2. SSL证书错误
**可能原因**:
- 证书文件路径错误
- 证书过期
- 域名不匹配

**解决方案**:
```bash
# 检查证书文件
ls -la nginx/ssl/

# 重新生成证书
./scripts/configure-domain.ps1 -DomainName "your-domain.com" -UseLetsEncrypt:$false
```

### 3. Nginx配置错误
**可能原因**:
- 配置文件语法错误
- 文件权限问题

**解决方案**:
```bash
# 检查配置语法
docker exec yiqi-nginx nginx -t

# 重新加载配置
docker exec yiqi-nginx nginx -s reload
```

## 📞 技术支持

如果遇到配置问题，请：

1. 检查本文档的常见问题部分
2. 查看Nginx错误日志：`docker logs yiqi-nginx`
3. 联系技术支持团队

---

**易骑公会技术团队** - 让游戏更有趣，让公会更温暖 🎮✨